# Nimbus AI

Nossa solução para a Global Solution consiste em uma aplicação voltada para a previsão de possíveis desastres naturais, levando em consideração a localização do usuário.

A aplicação coleta dados atualizados da previsão do tempo e a posição geográfica do usuário, utilizando essas informações junto a um modelo de inteligência artificial para prever a chance de ocorrência de desastres naturais em sua região.

Com base nessa previsão, o sistema envia alertas classificados em três níveis: baixo, médio e grave — permitindo avisar cada pessoa com precisão e antecedência.

Além disso, o usuário poderá adicionar grupos de localização, como a casa de familiares, o local de trabalho ou outros pontos de interesse. Dessa forma, ele receberá alertas personalizados para essas regiões também, ajudando na prevenção e no planejamento diante de possíveis enchentes ou outros eventos climáticos extremos.

Veja o pdf para a solução no repositório!

Veja o notebook em src/GSNimbus.ipynb

## Vídeo

https://youtu.be/0_y8_IiBZbk

## Observações
- Api Flask rodando na porta 5000
- Usamos docker para rodar, para isso, execute:

```
docker build -t nimbus-ai .
```
Depois execute: 

```
docker run --name nimbus-ai -d -p 5000:5000 --network nimbus-network nimbus-ai
```
