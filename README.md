# Back-end Onboarding

## Banco de dados

### Criando e rodando banco

```bash
cd Docker_onboarding
sudo docker build -f Dockerfile-db -t mysql_db .
sudo docker run -p 3306:3306 -d --name banco_onboarding -v mysql-volume:/var/lib/mysql mysql_db
```

### Rodando

```bash
sudo docker start banco_onboarding
```