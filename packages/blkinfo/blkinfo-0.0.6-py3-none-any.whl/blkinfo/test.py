#!/usr/bin/env python3

import json

from filters import BlkDiskInfo
from errors import NoLsblkFound



def main():
   myblkd = BlkDiskInfo()
   filters = {
      'tran': 'iscsi'
   }

   try:
      all_my_disk = myblkd.get_disk_list()
   except Exception as e:
      print(e)

   json_output = json.dumps(all_my_disk)
   print(json_output)



main()

