import random
import re
import io
import os
import argparse
import logging
import coloredlogs
import time
import asyncio
import sys
import binascii

from monero_serialize.helpers import ArchiveException
from monero_serialize.xmrtypes import TxExtraPubKey, TxExtraNonce, TxExtraAdditionalPubKeys, TxDestinationEntry

from monero_glue.hwtoken import misc
from monero_glue.xmr import wallet, crypto, monero
from monero_glue.xmr.monero import XmrNoSuchAddressException, generate_key_image_helper_precomp
from monero_glue.xmr.sub import addr
from monero_glue.xmr.sub.creds import AccountCreds

logger = logging.getLogger(__name__)
coloredlogs.CHROOT_FILES = []
coloredlogs.install(level=logging.DEBUG, use_chroot=False)


def generate_key_image_ex(
    creds,
    subaddresses,
    out_key,
    tx_public_key,
    additional_tx_public_keys,
    real_output_index,
):
    recv_derivation = crypto.generate_key_derivation(tx_public_key, creds.view_key_private)

    additional_recv_derivations = []
    for add_pub_key in additional_tx_public_keys:
        additional_recv_derivations.append(
            crypto.generate_key_derivation(add_pub_key, creds.view_key_private)
        )

    subaddr_recv_info = monero.is_out_to_acc_precomp(
        subaddresses,
        out_key,
        recv_derivation,
        additional_recv_derivations,
        real_output_index,
    )
    if subaddr_recv_info is None:
        raise XmrNoSuchAddressException()

    xi, ki = generate_key_image_helper_precomp(
        creds, out_key, subaddr_recv_info[1], real_output_index, subaddr_recv_info[0]
    )
    return xi, ki, recv_derivation, subaddr_recv_info


class TestGen(object):
    def __init__(self):
        self.args = None
        self.dest_keys = None  # type: AccountCreds
        self.cur_keys = None  # type: AccountCreds
        self.cur_subs = {}
        self.dest_subs = {}

        self.add_additionals = False
        self.dest_sub_major = 0

    async def process(self, idx, inp):
        is_stdin = False
        if inp == b"-":
            file = getattr(sys.stdin, "buffer", sys.stdin)
            is_stdin = True
        else:
            file = open(inp, "rb")

        try:
            logger.debug("Processing: %s" % inp)
            data = file.read()
            unsigned_tx = await wallet.load_unsigned_tx(self.cur_keys.view_key_private, data)

            if self.args.desc:
                await self.describe(inp, unsigned_tx, self.cur_keys, self.cur_subs)

            if self.dest_keys is None:
                return

            new_unsigned = await self.rekey_unsigned(unsigned_tx)

            new_bin = await wallet.dump_unsigned_tx(self.dest_keys.view_key_private, new_unsigned)

            if self.args.output:
                nbase = 'output.bin' if is_stdin else os.path.basename(inp)
                nbase_fname, nbase_ext = os.path.splitext(nbase)
                if self.args.suffix:
                    nbase_fname += self.args.suffix

                nbase = nbase_fname + nbase_ext
                ndest = os.path.join(self.args.output, nbase)

                if self.args.desc:
                    await self.describe(ndest, new_unsigned, self.dest_keys, self.dest_subs)

                with open(ndest, 'wb') as fh:
                    fh.write(new_bin)
                logger.info('Result written to: %s' % ndest)

            else:
                sys.stdout.buffer.write(new_bin)

        except ArchiveException as ae:
            logger.error(ae)
            logger.error(ae.tracker)

        finally:
            if not is_stdin:
                file.close()

    async def analyze_input(self, keys, subs, inp):
        subs = subs if subs else {}
        real_out_key = inp.outputs[inp.real_output][1]
        out_key = crypto.decodepoint(real_out_key.dest)
        tx_key = crypto.decodepoint(inp.real_out_tx_key)
        additional_keys = [
            crypto.decodepoint(x) for x in inp.real_out_additional_tx_keys
        ]

        res = generate_key_image_ex(keys, subs, out_key,
            tx_key,
            additional_keys,
            inp.real_output_in_tx_index,)

        xi, ki, recv_derivation, subaddr_recv_info = res
        sub_idx = subaddr_recv_info[0]
        return sub_idx

    async def reformat_out(self, out):
        res = misc.StdObj(amount=out.amount,
                          addr=addr.build_address(out.addr.m_spend_public_key,
                                                  out.addr.m_view_public_key),
                          is_subaddress=out.is_subaddress)
        return res

    async def reformat_outs(self, dsts):
        out_txs2 = []
        for o in dsts:
            out_txs2.append(await self.reformat_out(o))
        return out_txs2

    async def describe(self, inp, unsigned_txs, keys, key_subs):
        print('\nInp: %s, #txs: %s' % (inp, len(unsigned_txs.txes)))
        for txid, tx in enumerate(unsigned_txs.txes):
            srcs = tx.sources
            dsts = tx.splitted_dsts
            extra = tx.extra
            change = tx.change_dts
            account = tx.subaddr_account
            subs = tx.subaddr_indices
            amnt_in = sum([x.amount for x in srcs])
            amnt_out = sum([x.amount for x in dsts])
            fee = amnt_in - amnt_out
            n_inp_additional = sum([1 for x in srcs if len(x.real_out_additional_tx_keys) > 0])

            change_addr = addr.build_address(change.addr.m_spend_public_key, change.addr.m_view_public_key) if change else None
            out_txs2 = await self.reformat_outs(dsts)

            num_stdaddresses, num_subaddresses, single_dest_subaddress = addr.classify_subaddresses(out_txs2, change_addr)

            print('  tx: %s, #inp: %2d, #inp_add: %2d, #out: %2d, acc: %s, subs: %s, '
                  'xmr_in: %10.6f, xmr_out: %10.6f, fee: %10.6f, change: %10.6f, out_clean: %10.6f'
                  % (txid, len(srcs), n_inp_additional, len(dsts),
                     account, subs,
                     wallet.conv_disp_amount(amnt_in),
                     wallet.conv_disp_amount(amnt_out),
                     wallet.conv_disp_amount(fee),
                     wallet.conv_disp_amount(change.amount) if change else 0,
                     wallet.conv_disp_amount((amnt_out - change.amount) if change else amnt_out),
                     ))
            print('  Out: num_std: %2d, num_sub: %2d, single_dest_sub: %s'
                  % (num_stdaddresses, num_subaddresses, 1 if single_dest_subaddress else 0))

            accounts = set()
            subs = set()
            for inp in srcs:
                res = await self.analyze_input(keys, key_subs, inp)
                accounts.add(res[0])
                if res != (0, 0):
                    subs.add(res)

            print('  Ins: accounts: %s, subs: %s' % (accounts, len(subs)))

            extras = await monero.parse_extra_fields(extra)
            extras_val = []
            for c in extras:
                if isinstance(c, TxExtraPubKey):
                    extras_val.append('TxKey')
                elif isinstance(c, TxExtraNonce):
                    extras_val.append('Nonce: %s' % binascii.hexlify(c.nonce).decode('ascii'))
                elif isinstance(c, TxExtraAdditionalPubKeys):
                    extras_val.append('AdditionalTxKeys: %s' % len(c.data))
                else:
                    extras_val.append(str(c))
            print('  Extras: %s' % ', '.join(extras_val))

    async def primary_change_address(self, key, account):
        D, C = monero.generate_sub_address_keys(
            key.view_key_private,
            crypto.scalarmult_base(key.spend_key_private),
            account,
            0,
        )
        return misc.StdObj(
            view_public_key=crypto.encodepoint(C),
            spend_public_key=crypto.encodepoint(D),
        )

    async def adjust_change(self, tx):
        logger.debug('Change addr adjust')
        out_txs2 = await self.reformat_outs(tx.splitted_dsts)
        change_dts = await self.reformat_out(tx.change_dts) if tx.change_dts else None
        change_idx = addr.get_change_addr_idx(out_txs2, change_dts)
        if change_idx is None:
            return

        change_addr = await self.primary_change_address(self.dest_keys, self.dest_sub_major)
        tx.change_dts.addr.m_spend_public_key = change_addr.spend_public_key
        tx.change_dts.addr.m_view_public_key = change_addr.view_public_key

        tx.splitted_dsts[change_idx].addr.m_spend_public_key = change_addr.spend_public_key
        tx.splitted_dsts[change_idx].addr.m_view_public_key = change_addr.view_public_key

    async def amplify_outs(self, tx):
        lst = tx.splitted_dsts[-1]
        orig_amount = lst.amount
        partial = orig_amount // (self.args.outs + 1)
        amnt_sum = partial
        lst.amount = partial

        for i in range(1, self.args.outs + 1):
            is_lst = i >= self.args.outs
            new_amnt = orig_amount - amnt_sum if is_lst else partial
            amnt_sum += partial
            new_tx = TxDestinationEntry(amount=new_amnt, is_subaddress=lst.is_subaddress, addr=lst.addr)
            tx.splitted_dsts.append(new_tx)

    async def rekey_unsigned(self, unsigned_txs):
        for tx in unsigned_txs.txes:
            tx.use_bulletproofs = False
            logger.debug(
                "Transaction with %s inputs, %s outputs, %s mix ring"
                % (len(tx.sources), len(tx.splitted_dsts), len(tx.sources[0].outputs))
            )

            for inp in tx.sources:
                self.rekey_input(inp, self.cur_keys, self.cur_subs, self.dest_keys, self.dest_subs)

            if tx.change_dts and tx.subaddr_account != self.dest_sub_major:
                await self.adjust_change(tx)

            tx.subaddr_account = self.dest_sub_major
            tx.subaddr_indices = self.args.minors

            if self.args.outs is not None:
                await self.amplify_outs(tx)

        return unsigned_txs

    def rekey_input(self, inp, keys, subs=None, new_keys=None, new_subs=None):
        subs = subs if subs else {}
        real_out_key = inp.outputs[inp.real_output][1]
        out_key = crypto.decodepoint(real_out_key.dest)
        tx_key = crypto.decodepoint(inp.real_out_tx_key)
        additional_keys = [
            crypto.decodepoint(x) for x in inp.real_out_additional_tx_keys
        ]

        logger.debug('Current out key: %s' % binascii.hexlify(real_out_key.dest))
        secs = monero.generate_key_image_helper(
            keys,
            subs,
            out_key,
            tx_key,
            additional_keys,
            inp.real_output_in_tx_index,
        )
        xi, ki, di = secs

        need_additional = additional_keys is not None and len(additional_keys) > 0
        is_dst_sub = self.dest_sub_major != 0 and (self.args.minors[0] != 0 or len(self.args.minors) > 1)
        logger.debug('Is dst sub: %s, need additional: %s' % (is_dst_sub, need_additional))

        if is_dst_sub and self.add_additionals:
            need_additional = True

        if is_dst_sub:
            rand_minor = random.choice(self.args.minors)
            m = monero.get_subaddress_secret_key(new_keys.view_key_private, major=self.dest_sub_major, minor=rand_minor)
            M = crypto.scalarmult_base(m)
            d = crypto.sc_add(m, new_keys.spend_key_private)
            D = crypto.point_add(new_keys.spend_key_public, M)
            C = crypto.scalarmult(D, new_keys.view_key_private)

        if not need_additional and not is_dst_sub:
            # real_out_key.dst = Hs(R*new_a || idx)G + newB
            r = crypto.random_scalar()
            tx_key = crypto.scalarmult_base(r)
            new_deriv = crypto.generate_key_derivation(new_keys.view_key_public, r)
            new_out_pr = crypto.derive_secret_key(new_deriv, inp.real_output_in_tx_index, new_keys.spend_key_private)
            new_out = crypto.scalarmult_base(new_out_pr)
            real_out_key.dest = crypto.encodepoint(new_out)

        elif not need_additional and is_dst_sub:
            # real_out_key.dst = Hs(r*C || idx)G + newB, R=rD
            r = crypto.random_scalar()
            tx_key = crypto.scalarmult(D, r)
            new_deriv = crypto.generate_key_derivation(C, r)
            new_out_pr = crypto.derive_secret_key(new_deriv, inp.real_output_in_tx_index, d)
            new_out = crypto.scalarmult_base(new_out_pr)
            real_out_key.dest = crypto.encodepoint(new_out)

        else:
            r = crypto.random_scalar()
            tx_key = crypto.scalarmult_base(r)

            gen_additionals = min(2, inp.real_output_in_tx_index + 1)
            if additional_keys is None or len(additional_keys) < gen_additionals:
                additional_keys = [crypto.scalarmult_base(crypto.random_scalar()) for _ in range(gen_additionals)]

            ri = crypto.random_scalar()
            if is_dst_sub:
                add_tx = crypto.scalarmult(D, ri)
                new_deriv = crypto.generate_key_derivation(C, ri)
                new_out_pr = crypto.derive_secret_key(new_deriv, inp.real_output_in_tx_index, d)
                new_out = crypto.scalarmult_base(new_out_pr)
                if not crypto.point_eq(new_out, crypto.derive_public_key(new_deriv, inp.real_output_in_tx_index, D)):
                    raise ValueError('Invalid txout computation')

            else:
                add_tx = crypto.scalarmult_base(ri)
                new_deriv = crypto.generate_key_derivation(new_keys.view_key_public, r)
                new_out_pr = crypto.derive_secret_key(new_deriv, inp.real_output_in_tx_index,
                                                      new_keys.spend_key_private)
                new_out = crypto.scalarmult_base(new_out_pr)

            additional_keys[inp.real_output_in_tx_index] = add_tx
            real_out_key.dest = crypto.encodepoint(new_out)

        inp.real_out_tx_key = crypto.encodepoint(tx_key)
        inp.real_out_additional_tx_keys = [crypto.encodepoint(x) for x in additional_keys]

        logger.debug('New pub: %s' % binascii.hexlify(real_out_key.dest))

        # Self-check
        secs = monero.generate_key_image_helper(
            new_keys,
            new_subs,
            crypto.decodepoint(real_out_key.dest),
            tx_key,
            additional_keys,
            inp.real_output_in_tx_index,
        )
        return inp

    def precompute_subaddr(self, keys, subs, major_cnt=10, minor_cnt=200):
        if keys is None:
            return None
        for i in range(major_cnt):
            monero.compute_subaddresses(keys, i, list(range(0, minor_cnt)), subs)

    def parse_keys(self, keyvar, ktype="current"):
        if keyvar is None:
            return None
        if len(keyvar) != 2 * 2 * 32:
            raise ValueError(
                "Keys for the %s destination length invalid. Format: SpendKey || ViewKey hexcoded"
                % ktype
            )
        keys_bin = binascii.unhexlify(keyvar)
        spend_key = crypto.decodeint(keys_bin[:32])
        view_key = crypto.decodeint(keys_bin[32:64])

        return AccountCreds.new_wallet(view_key, spend_key)

    async def work(self):
        self.cur_keys = self.parse_keys(self.args.current)
        self.dest_keys = self.parse_keys(self.args.dest, "destination")
        self.dest_sub_major = self.args.major
        self.add_additionals = self.args.add_extra
        self.precompute_subaddr(self.cur_keys, self.cur_subs)
        self.precompute_subaddr(self.dest_keys, self.dest_subs)

        files = self.args.files if self.args.files and len(self.args.files) else [b"-"]
        for idx, line in enumerate(files):
            await self.process(idx, line)

    async def main(self):
        parser = argparse.ArgumentParser(
            description="Test generator - changing unsigned transactions"
        )
        parser.add_argument(
            "--dest",
            default=None,
            required=False,
            help="Destination address to transform to",
        )

        parser.add_argument(
            "--current", default=None, required=True, help="Current destination address"
        )

        parser.add_argument(
            "--output",
            default=None,
            help="Output directory to write results to",
        )

        parser.add_argument(
            "--major",
            default=0,
            type=int,
            help="Destination major address index",
        )

        parser.add_argument(
            "--minors",
            default=[0],
            type=int,
            nargs="*",
            help="Destination minor address index",
        )

        parser.add_argument(
            "--desc",
            dest="desc",
            default=False,
            action="store_const",
            const=True,
            help="Generate test file descriptors",
        )

        parser.add_argument(
            "--suffix",
            dest="suffix",
            default="",
            help="Generated tsx files suffix",
        )

        parser.add_argument(
            "--outs",
            dest="outs",
            default=None,
            type=int,
            help="Amplify the last output to outs - increases tx outputs",
        )

        parser.add_argument('--add-extra', dest='add_extra', action='store_const', const=True, default=False,
                            help='Adds additional tx keys')

        parser.add_argument(
            "files",
            metavar="FILE",
            nargs="*",
            help="files to read, if empty, stdin is used",
        )
        self.args = parser.parse_args()
        return await self.work()


async def amain():
    tgen = TestGen()
    res = await tgen.main()
    sys.exit(res)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())
    loop.close()


if __name__ == "__main__":
    main()
