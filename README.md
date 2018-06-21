
# Autofalante
Como proposta de trabalho para a disciplina de Sistemas Operacionais, o projeto Autofalante é um administrador de sistema de som caseiro. Ele consiste em um módulo MP3 ligado a um módulo Wifi, programado através de um Arduino, e em um website. O usuário acessa o website indicando quais músicas quer colocar na fila ou quais playlists deseja ouvir e o módulo Wi-fi faz o acesso ao mesmo servidor para buscar a músicas que devem ser tocadas.   
Para usuários não cadastrados a única funcionalidade é colocar músicas na fila de execução. Para usuários cadastrados, é possível criar, executar, apagar e compartilhar playlists, além de executar imediatamente as músicas.

# Dependências 
Python 3.6  
Django 2.0  
Módulo Wi-fi ESP8266 e biblioteca esp8266.h   
Módulo DFPlayer Mini e biblioteca DFRobotDFPlayerMini.h   

# O que foi usado pelo grupo
O framework Django para desenvolvimento web e todos os arquivos padrão instalados nele, incluindo as interfaces para renderização de páginas HTML, o SGBD SQLite3, a interface para geração de formulários em HTML e o mapeamento de URLs, além das aplicações já prontas auth e admin para autenticação e lado admin do website, respectivamente.  
Para o ESP e o DFPlayer, as bibliotecas indicadas foram usadas para comunicação Wi-fi e para realização dos comandos do módulo MP3.

# O que foi desenvolvido pelo grupo
Todo o back-end e front-end do site, junto com a administração do banco de dados para criação e administração das playlists. O esquema para busca das músicas a serem tocadas no servidor, o gerenciamento da fila de comandos e da fila de músicas a serem tocadas. O algoritmo para colocar as playlists em execução, a comunicação ESP-DFPlayer e por fim a construção de uma caixa de som e de um circuito ligando a saída do DFPlayer a um amplificador e a ligação desse amplificador com o alto-falante.

# Arquitetura
![alt text](https://github.com/bvm810/Sistemas-Operacionais/blob/master/Arquitetura.PNG)  
O usuário faz os pedidos ao servidor, e em seguida o módulo Wi-fi busca esses pedidos e os repassa ao DFP de modo a tocar as músicas na caixa de som. Os arquivos .mp3 ficam armazenados em um SD Card inserido dentro do DFP e por isso não foram representados.

# Descrição Técnica
Através do framework Django, foi criado um site para o acesso do usuário ao sistema de gerenciamento da caixa de som. O Django é responsável por renderizar as páginas e formulários HTMLs criados usando alguns parâmetros presentes na URL acessada (arquivo views.py). Devido a isso, é possível, ao renderizar páginas específicas, fazer alterações no banco de dados (cujos modelos estão em models.py), com a criação, deleção e compartilhamento de playlists e também enviar músicas para a fila de execução ou diretamente para a fila de comandos (música sendo executada imediatamente).    
Essas duas filas são criadas colocando o código numérico previamente atribuído de todas as músicas que tiverem sido selecionadas (flags in_line e executing do BD) em uma outra página web, que é acessada pelo ESP usando a biblioteca "esp8266.h" usando GET. Tendo os códigos das músicas em mãos, o ESP manda os comandos correspondentes aos códigos para o módulo DFPlayer usando a biblioteca "DFRobotDFPlayerMini.h" e por fim o módulo MP3 executa os comandos pedidos.    
No caso em que há mais de um comando ou mais de uma música na página correspondente à fila de comandos ou de execução, os comandos/músicas são armazenados num vetor que funciona como a FIFO necessária. Comandos/músicas enviados primeiro são retirados primeiro do vetor de armazenamento, que funciona portanto como um buffer de fila.    
Como mencionado na introdução, esse sistema foi projetado para funcionar compartilhando a caixa de som tanto em situações com poucos usuário em uso doméstico, quanto para uso com muitas pessoas, como por exemplo em uma festa. Então as funcionalidades de criação, execução e deleção de playlists só estão disponíveis para usuários cadastrados. Os demais usuários podem somente adicionar músicas na fila.  
Para o login, foi utilizada a aplicação auth que já vem instalada no Django e já possui interface de usuário e autenticação de login. No uso real do sistema, a pessoa que comprasse iria primeiramente usando o admin cadastrar seu próprio usuário, e em seguida manualmente fazer o cadastro dos demais usuários do sistema.

