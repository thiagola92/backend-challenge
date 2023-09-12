# Desafio
[Instruções](CHALLENGE.md)

# Requisitos
O Docker Compose carrega variáveis de ambiente do arquivo `.env`,  então é preciso criar este arquivo pelo menos uma vez.  

O projeto disponibiliza o template `.env.template` para ser usado como base. Recomendo criar uma cópia do arquivo:  

```
cp .env.template .env
```

# Utilização
```
sudo docker compose up
```

Acesso URL: http://127.0.0.1:8000  
PostgreSQL URI: `postgresql://username:password@127.0.0.1:5432/username`  

### Observações
Utilizando as informações providênciadas no `.env`, o seguinte é criado:  
- Usuário para a API (`API_USERNAME`, `API_PASSWORD`)  
- Admin no PostgreSQL (`POSTGRES_USER`, `POSTGRES_PASSWORD`)  