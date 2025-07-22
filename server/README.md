# syslabmgr - go

## Build

```bash
go build -o ../syslabmgr
```

## run

```
./syslabmgr
```

## Docker

```bash
docker build -t syslabmgr .
docker run -d -p 9101:9101 --name my-syslabmgr --restart unless-stopped --memory 512m syslabmgr
```
