# Encurtador de URLs

---

## Requisitos

[x] O serviço irá receber inicialmente como parâmetro uma URL que deverá ser encurtada seguindo as seguintes regras:

[x] Mínimo de 5 e máximo de 10 caracteres.

[x] Apenas letras e números.

[x] A url retornada deverá ser salva no banco de dados

[] Possuir um prazo de validade (tempo a definir)

[x] Receber uma url encurtada, deverá fazer o redirecionamento para a url salva no banco.

### Exemplo ao encurtar

- Seu sitema recebe uma chamada para encurtar a url `backendbrasil.com.br` e retorna o seguinte json

```json
{
  newUrl: "http://localhost:8081/abc123ab";
}
```

### Exemplo ao redirecionar

- Ao receber uma chamada para `http://localhost:8081/abc123ab` você irá retorna um redirecionamento para a url salva no banco (`backendbrasil.com.br`), caso não seja encontrada, retornar HTTP 404
