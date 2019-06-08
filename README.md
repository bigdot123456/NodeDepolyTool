# NodeDepolyTool
./gman --datadir ./chaindata --syncmode "full" --manAddress "MAN.CrsnQSJJfGxpb2taGhChLuyZwZJo" --testmode Yeying1021!@# --entrust ./entrust.json 

1.--manAddress "MAN.CrsnQSJJfGxpb2taGhChLuyZwZJo" 地址更改为本机A1账户
2.--entrust ./entrust.json 将"./entrust.json" 改为自己的entrust文件路径
3.--testmode Yeying1021!@#  将"Yeying1021!@#"改为自己的entrust文件密码

 kill -9  `ps -ef | grep  -v grep  | grep  gman | grep 'networkid'  | awk '{print $2}'`   杀死gman

/home/matrix/gman --datadir /home/matrix/chaindata  init /home/matrix/MANGenesis.json  初始化GMAN

/home/matrix/gman --datadir /home/matrix/chaindata --rpc --rpcaddr 0.0.0.0 --rpccorsdomain '*' --networkid 666 --debug --verbosity 5 --manAddress MAN.2UMgrmoFTq2urw1xKBgx5XfpFnhR3 --entrust /home/matrix/entrust.json --gcmode archive --outputinfo 1 --syncmode 'full'  启动GMAN

/home/matrix/gman  --datadir /home/matrix/chaindata aes --aesin Signature.json --aesout /home/matrix/entrust.json  加密keystore
