#coding: utf-8
from binaryninja import *
import re

__funcList={}
def resolve(bv,curaddr):
  disas = re.split(" +",bv.get_disassembly(curaddr))
  if disas[0]!="call":
    log.log_error("is not call instruction.")
    return -1
  inputAddr = int(disas[1],16)

  rdyn=bv.get_section_by_name(".rel.dyn")
  dsym=bv.get_section_by_name(rdyn.linked_section)
  dstr=bv.get_section_by_name(dsym.linked_section)

  br = BinaryReader(bv)

  max=(rdyn.end-rdyn.start)/8
  idx = None
  # .rel.pltを参照する。
  # 入力されたアドレスに一致するエントリを探し
  # .dynsymのインデックスを解決する
  addr = 0
  for i in xrange(max):
    rptr=(i*8)+rdyn.start
    br.seek(rptr)
    addr=br.read32()
    if(inputAddr==addr):
      rptr=(i*8)+rdyn.start+5 # 5 = 構造体の5バイト目
      br.seek(rptr)
      idx=br.read8()
  # .dynsymを参照し、インデックスを足して.dynstrのオフセットを得る
  if idx==None:
    log.log_error("Unknown function")
    return -1
  rptr=dsym.start+(16*idx)
  br.seek(rptr)
  symstrOffset=br.read32()
  # .dynstrでシンボル名を見つける
  rptr=dstr.start+symstrOffset
  br.seek(rptr)
  symstr=br.read(bv.get_strings(rptr,1)[0].length)
  log.log_info("symbol:"+symstr)
  if symstr not in __funcList:
    __funcList[symstr] = disas[1]
  arch=Architecture["x86"]
  bin = arch.assemble("call "+str(int(__funcList[symstr],16)-curaddr))[0]
  bw = BinaryWriter(bv)
  bw.seek(curaddr)
  if bw.write(bin)==True:
    log.log_info("success")
  else:
    log.log_error("error")
