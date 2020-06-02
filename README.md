# FaceBlock
Blockchain based social network that allows people to interact each others

This application is based on this repo [Blockchain](https://github.com/ManuGS2/Blockchain)

first approach is set a redis list with block hashes 
and for every hash use it as value for a redis dict that will 
contain all block info

Lists in redis are linked lists

Que es un transaccion
* Post
* reaccion

Que contiene un transaccion
* Autor
* La hora (timestamp)
* tipo de transaccion
* contenido

contenido para un post
* Texto

Contenido para una reaccion
* id del post
* tipo de reaccion

Cada cuando se va a minar
* Cada 5 transacciones

Algoritmo de minado
*  Verificar si es un comment positivo

transaction = {
  'author': "some author",
  'content': "some content",
  'timestamp': "some time"
}
