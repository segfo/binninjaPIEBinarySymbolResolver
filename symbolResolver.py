#coding: utf-8
from binaryninja import *

def resolve(bv,addr):
  rdyn=bv.get_section_by_name(".rel.dyn")
  dsym=bv.get_section_by_name(rdyn.linked_section)
  dstr=bv.get_section_by_name(dsym.linked_section)

  br = BinaryReader(bv)

  inputAddr = get_address_input("input me","address input")
  max=(rdyn.end-rdyn.start)/8
  idx = None
  # .rel.pltを参照する。
  # 入力されたアドレスに一致するエントリを探し
  # .dynsymのインデックスを解決する
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
  log.log_info("symbol:"+br.read(bv.get_strings(rptr,1)[0].length))
