### Protocol Buffer

generate source

```shell
protoc -I=. --python_out=./ ./addressbook.proto
```

```shell
python protobuf_write.py output.txt
```

```shell
python protobuf_read.py output.txt
```
