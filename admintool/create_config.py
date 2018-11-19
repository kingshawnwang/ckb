#!/usr/bin/env python
# coding=utf-8

import os
import sys
import binascii
import ast

def make_config():
    nid = int(sys.argv[2])
    path = os.path.join(sys.argv[1],"node" + str(nid))
    keypairs_path = os.path.join(sys.argv[1], "bls.keypairs")
    keypairs_f = open(keypairs_path, "r")
    keypairs = keypairs_f.readlines()
    config_name = "config"
    dump_path = os.path.join(path, config_name)
    f = open(dump_path, "w")
    key = keypairs[nid * 3]
    f.write("miner_private_key = \"0x" + ''.join(format(x, '02x') for x in ast.literal_eval(key)) + "\"\n")
    secret_path = os.path.join(path, "signer_privkey")
    secret_key = open(secret_path, "r")
    key = secret_key.read()
    secret_key.close()
    f.write("signer_private_key = \"0x" + key + "\"\n")
    f.write("[logger]" + "\n")
    f.write("file = \"/tmp/nervos" + str(nid) +".log\"\n")
    f.write("filter = \"main=info,miner=info,chain=info\"\n")
    f.write("color = true\n")
    
    #generate keypairs
    signer_auth_path = os.path.join(sys.argv[1], "signer_authorities")
    signer_auth = open(signer_auth_path, "r")

    i = 1
    while True:
        signer_key = signer_auth.readline().strip('\n')
        proof_key = ''.join(format(x, '02x') for x in ast.literal_eval(keypairs[i]))
        proof_g = ''.join(format(x, '02x') for x in ast.literal_eval(keypairs[i+1]))
        if (not signer_key) or (not proof_key):
            break
        f.write("[[key_pairs]]" + "\n")
        f.write("proof_public_key = \"0x" + proof_key + "\"\n")
        f.write("proof_public_g = \"0x" + proof_g + "\"\n")
        f.write("signer_public_key = \"0x" + signer_key + "\"\n")
        i += 3

    signer_auth.close()
    keypairs_f.close()
    f.close()

make_config()