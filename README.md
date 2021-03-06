# BrainMRISeg
Projeto final para a disciplina de Processamento de Imagens ICMC-USP

## Título
**Segmentação assistida de regiões de interesse em imagens de ressonância magnética cerebral**

### Integrantes
>**Iury Andrade** 

>**Rodrigo Duarte**


### Resumo
Este projeto almeja trabalhar com segmentação de regiões de interesse em imagens médicas a fim de realizar a segmentação de regiões de maneira assistida, a partir de pontos iniciais de interesse de um especialista de domínio. É desejado entender as situações e diferentes métodos de segmentação que podem ser aplicados, realizando-se um comparativo entre diferentes abordagens, e também comparativamente com resultados de segmentações realizadas de maneira manual por especialistas.

As imagens são provenientes de ressonância magnética (IRM) da região cerebral, de topologia definida por uma malha/grid tridimensional, onde serão extraídas partições (slices) específicos da aquisição, obtendo-se finalmente uma imagem bidimensional para ser processada. Imagens médicas, podem acabar sendo de difícil execução em relação a segmentação, possuindo padrões complexos e diversos casos limítrofes que podem ocasionar errôneas descontinuidades. Ao mesmo tempo, realizar a segmentação manual dessas estruturas é custoso por exigir profissionais especializados, trabalhoso, demorado e entendiante, sendo assim bastante beneficiado por métodos que auxiliem na segmentação assistida a partir de localizações iniciais.

### Objetivo principal
Utilizando algoritmos de segmentação como os mencionados posteriormente,
 a ideia principal é obter segmentações de interesse a partir de pontos 
dados pelo operador humano para uma sequência de _slices_ anteriores, posteriores, ou ambos, de um _slice_ de referência com a lesão de interesse, de qualidade equivalente as realizadas em um
 processo inteiramente manual por um especialista. Dado as lesões comumente se manifestarem por multiplos _slices_, a segmentação manual é cansativa, tediosa e custosa. A automatização desse processo tem grande valor prático para essa atividade ao obter máscaras de segmentação de aproximação satisfatória.
 Adicionalmente, também objetivamos a exploração de como procedimentos de
 pré-processamento podem auxiliar em melhores resultados na etapa de 
segmentação. Por fim, é de interesse realizar uma análise comparativa 
entre os métodos de segmentação explorados, bem como entre os resultados
 das segmentações

### Descrição do conjunto de Dados
O conjunto de dados adotado neste projeto é o [EPISURG](https://rdr.ucl.ac.uk/articles/dataset/EPISURG_a_dataset_of_postoperative_magnetic_resonance_images_MRI_for_quantitative_analysis_of_resection_neurosurgery_for_refractory_epilepsy/9996158/1) de imagens de ressonância magnética cerebrais. Este conjunto é composto por 430 aquisições posteriores a intervenção cirúrgicas de pacientes com epilepsia, dos quais 268 também possuem imagens pré-operatórias. Ainda, um subgrupo de pacientes possuem também máscaras de segmentação das regiões extraídas durante a intervenção cirúrgica, sendo as máscaras especificadas por até três diferentes especialistas. Este último subgrupo com máscaras de segmentação são o conjunto de imagens adotadas durante este projeto.

O conjunto de dados esta organizado de maneira semelhante ao padrão BIDS, comumente adotado para este tipo de dados, possuindo um arquivo `subjects.csv` com a listagem dos pacientes e informações sobre a localização do procedimento, sexo e presença ou ausência de imagens pré-operatórias. Cada paciente do conjunto possui ao menos uma MRI do tipo T1. 

As aquisições MRI representam a informação volumétrica distribuída em uma malha/grid tridimensional. Sendo assim, diferentemente de imagens convencionais que são representadas por pixeis que medem intensidade de luz, as MRI são representadas por voxeis que representam valores de intensidade volumétrica. Contudo, para fins de visualização, podemos observar estas imagens como imagens convencionais em tons de cinza.

#### Exemplos de imagens do conjunto de dados
As imagens de MRI podem ser adquiridas por meio de diferentes modalidades, sendo as presentes no conjunto de dados imagens MRI do tipo T1. Nestas, as regiões mais claras na imagem representam as áreas de massa branca cerebral, enquanto as regiões mais cinzas as regiões de massa cinzenta. Ainda, demais líquidos como os fluidos cérebro-espinais e regiões “vazias” aparecem em tons mais escuros, aproximando-se do preto. Ossos aparecem como densas regiões claras. As imagens T1 são consideradas as mais anatômicas devido a característica de poderem ser observadas as regiões mais características e utilizadas como referencial do cérebro. 

Além de sua visualização como uma estrutura tridimensional, as MRIs podem ser observadas por meio de recortes específicos de fatias bidimensionais em locais de interesse. Essas fatias podem ser observadas de acordo com a perspetiva desejada: axial (visão como visto paralelo aos pés), coronal (visão como visto paralelo ao rosto) e sagital (visão como visto paralela ao comprimento do corpo). Estas perspectivas são apresentadas na Figura 1(a), (b) e (c), respectivamente 



!["Imagem exemplo na visão axial"](imgs/axial.png "Figura 1a: Imagem na perspectiva axial") 
!["Imagem exemplo na visão coronal"](imgs/coronal.png "Figura 1a: Imagem na perspectiva coronal")
!["Imagem exemplo na visão sagital"](imgs/sagital.png "Figura 1a: Imagem na perspectiva sagital")

Figura 1: Topo esquerdo: Imagem na perspectiva axial; Topo direito: Imagem na perspectiva coronal; Inferior esquerdo: Imagem na perspetiva sagital. Fonte: [EPISURG dataset](https://rdr.ucl.ac.uk/articles/dataset/EPISURG_a_dataset_of_postoperative_magnetic_resonance_images_MRI_for_quantitative_analysis_of_resection_neurosurgery_for_refractory_epilepsy/9996158/1)



------
Durante este trabalho, as MRI são exploradas e utilizadas em sua representação em fatias bidimensionais, em suas perspectivas axial, coronal e sagital (de acordo com a intenção do durante o momento da execução) e representadas em tons de cinza.
Para os métodos de segmentação, estamos interessados nas regiões como apresentado no detalhe da Figura 2. A seta aponta uma região extraída por procedimento cirúrgico, em tom escuro devido à ausência do tecido.

!["Detalhe de região com seta indicando local com massa cerebral extraída"](imgs/reg_mark.png "Detalhe de região com seta indicando local com massa cerebral extraída") 

Figure 2: Detalhe de região extraída durante procedimento cirurgico. Devido a ausência de massa cerebral, região se apresenta como uma tonalidade escura na imagem T1. Fonte: [EPISURG dataset](https://rdr.ucl.ac.uk/articles/dataset/EPISURG_a_dataset_of_postoperative_magnetic_resonance_images_MRI_for_quantitative_analysis_of_resection_neurosurgery_for_refractory_epilepsy/9996158/1)


------
O objetivo assim é obter máscaras de segmentação como apresentada nas imagens da Figura 3(b). 

!["Imagem exempo de IRM cerebral de região com região extraída, sem mascara de segmentação"](imgs/ImgSemMascara.png "Imagem exempo de IRM cerebral de região com região extraída, sem mascara de segmentação") 
!["Imagem exempo de IRM cerebral de região com região extraídae com mascara de segmentação"](imgs/ImgComMascara.png "Imagem exempo de IRM cerebral de região com região extraídae com mascara de segmentação")

Figura 3(a) Imagem exemplo de IRM cerebral de região extraída por meio de intervenção cirúrgica, sem máscara de segmentação; (b) Imagem exemplo de IRM cerebral de região com região extraída e com máscara de segmentação. Fonte: [EPISURG dataset](https://rdr.ucl.ac.uk/articles/dataset/EPISURG_a_dataset_of_postoperative_magnetic_resonance_images_MRI_for_quantitative_analysis_of_resection_neurosurgery_for_refractory_epilepsy/9996158/1)

## Etapas de execução do projeto
- ### Seleção do conjunto de dados
    - Dado todo o conjunto de imagens do conjunto [EPISURG dataset](https://rdr.ucl.ac.uk/articles/dataset/EPISURG_a_dataset_of_postoperative_magnetic_resonance_images_MRI_for_quantitative_analysis_of_resection_neurosurgery_for_refractory_epilepsy/9996158/1), a partir dos pacientes presentes no arquivo `subjects.csv`, informações inicias são construídas como um `Dataframe`;
    - O conjunto construído é filtrado para conter apenas exemplos que possuam ao menos uma máscara de segmentação presente. Cada paciente pode ter até um máximo de três máscaras providas por especialistas humanos, mas ao menos uma se faz necessária para comparativo como _ground-truth_. Os demais exemplos sem nenhuma máscara são descartados;
    - Os pacientes selecionados e filtrados tem os caminhos dos arquivos `.nii` (extensão para imagens de MRI) agregados aos seus dados no `Dataframe`, tanto para o arquivo MRI T1, como para as máscaras de segmentação.
    - Ao fim do processo têm-se o conjunto de dados pronto para uso nas demais etapas.
- ### Pré-processamento
    - Utilização de filtros suavizantes, como filtros de média, para retirada de ruídos e segmentar de maneira mais eficiente
    - Como as imagens estão em escala de cinza, limiarizar para a utilização de processos morfológicos sobre a imagem de forma a encontrar bordas e preenchelas. Limiarizar é utilizado também no processo de segmentação por regiões para a escolha de uma semente.
    - Utilizar matrizes das derivadas tanto na utilização da segmentação por watershed, quanto para detectar traços finos e grossos.
- ### Segmentação Chan-Vese
    - A ideia esta minimizar um funcional energia, como dito anteriormente.
    - O processo começa dizendo quem são os parametros para a segmentação.
    - Escolher a segmentação após as iterações.
    - Escolher um ponto adequado para pegar a parte conexa da segmentação.
    - Sobrepor a segmentação na imagem original para obter a imagem com máscara da segmentação.
- ### Segmentação Watershed
    - Uma imagem previamente pré-processada é utilizada como entrada para este método. Os pré-processamentos podem incluir os diversos procedimentos explicitados anteriormente, em especial a redução de ruídos, cálculo de gradientes para obtenção de mínimos locais e processos morfológicos para obter bordas/fronteiras bem estabelecidas;
    - Também é informado quais os marcadores inicias (sementes) para o início do processo. Dado o objetivo de segmentação guiada, essas sementes devem ser previamente informadas por um operador humano. Ao menos 3 sementes são necessárias: Uma do _background_ real da imagem MRI, isto é, a região que não contem voxeis referentes a região cerebral. Esta primeira semente é automaticamente definida pelo método como sendo o pixel (0, 0); uma semente da região interna do cérebro, porém fora da região de interesse; e uma última semente na região de interesse, sendo essa a região para qual de fato se deseja obter a máscara como resultado. As duas últimas sementes devem ser informadas pelo usuário;
    - O método _Watershed_ é executado a partir da imagem pré-processada e das sementes informadas, retornando as regiões segmentadas, cada qual com seu respectivo rótulo;
    - O segmento da região de interesse pode então ser aplicado como uma máscara sobre a imagem MRI, extraindo assim apenas a região de interesse.
- ### Avaliação e comparação dos resultados
    - Análises quantitativa por meio da obtenção de índices Dice de similaridade entre as segmentações geradas pelos métodos de segmentação e as máscaras humanas. O índice Dice de similaridade é amplamente para avaliar métodos de segmentação por meio da comparação de máscaras binárias. 
    - Análise qualitativa  visual das máscaras obtidas quando projetadas sobre a imagem de ressonância e lado a lado com as máscaras de especialistas.

----------------
## Métodos de Segmentação

Nesta seção são apresentados os conceitos gerais dos métodos de segmentação adotados neste projeto: segmentação Chan-Vese e segmentação Watershed. Estes métodos de segmentação foram selecionados por permitirem o uso de sementes (ou marcadores) em alguma etapa do seu processo, possibilitando assim o objetivo de segmentação assistida e inserção do conhecimento de um operador humano no processo automatizado da segmentação, indicando a região de interesse explicitamente. 

### Método Chan-Vese
Chan-Vese para contorno ativo é um método muito poderoso e flexível, permitindo segmentações de vários tipos de imagens, podendo ser bem útil quando métodos como thresholding ou gradientes não funcionem tão bem.

Tal modelo se baseia na ideia de minimizar um funcional energia, podendo ser reformulado como curvas de nível, tornando assim mais fácil de resolver o problema.

Como o objetivo é entender a análise de casos do método, apenas uma breve apresentação da ideia do método será mostrada.

Seja C uma curva, $C^{1}[0, 1]$ por partes. Vamos denotar por $\omega$ como região interna de C. Além disso, iremos denotar por $c_{1}$ a intensidade média dos pontos interiores e $c_{2}$ a intensidade externa a curva C.

O objetivo do método é minimizar o funcional energia

$F(c_{1}$, $c_{2}$, C$)$ = $\mu$*Comprimento(C) + $\lambda_{1}$ * $\int_{inside\ (C)}$ |Image$[x,y]$ - $c_{1}$|$^{2}dxdy$ + $\lambda_{2}$ * $\int_{outside\ (C)}$ |Image$[x,y]$ - $c_{2}$|$^{2}dxdy$

As iterações vem da abordagem de curvas de nível, que não será explicado aqui.


### Método Watershed

O método watershed de segmentação possui uma abordagem topológica, buscando agir de maneira semelhante a inundação de bacias por um agente líquido a partir de pontos de infiltração. Para tanto, uma imagem a ser segmentada é definida em três tipos de pontos: pontos que representam um mínimo local; pontos que, considerando o cair de uma gota d’água, está tenha alta probabilidade de rolar em direção ao mínimo local daquela região; e pontos limiares, onde a probabilidade da gota d’água rolar para qualquer um dos lados é igual. 

O mecanismo de funcionamento do Watershed é comparável a realizar a inundação de regiões a partir de um fluxo contínuo de água que emerge de determinados pontos, dispostos nas regiões de mínimos locais. Esta inundação é realizada de maneira paralela entre todas as bacias existentes. Em determinado momento, é esperado que as inundações de cada bacia alcancem um estado onde estejam prestes a se mesclar com outras bacias adjacentes. Neste momento, o método deve criar uma barreira que impeça esta mesclagem, dividindo de maneira determinante as bacias em segmentos distintos.

Desta forma, a aplicação da segmentação Watershed exige que a imagem de entrada tenha características que permitam esse processo ocorrer de forma adequada, isto é, as regiões precisam ter bordas mais ou menos definidas, e com intensidade nos valores dos pixeis na região interna as bordas que apresentem um mínimo local. Para tanto, processos morfológicos, como dilatação, _closing_, e aplicação de filtros para obtenção de bordas por meio de gradientes, são de imensa valia como etapas de pré-processamento. 

Os pontos onde se inicia o processo de inundação são chamados de sementes (ou marcadores). Tais sementes podem ser explicitamente definidas por um agente humano, de maneira a guiar o processo e direcionar regiões bases onde se deseja ter a formação de segmentos. Por tanto, o método Watershed é adequado para processos de segmentação onde é possível ou se deseja inserir informações _a priori_, provenientes de conhecimento de contexto e de especialistas de domínio. 

Por fim, devido ser um método que mistura conceitos de topologia, segmentação por limiar (_threshold_) e baseada em regiões, o Watershed agrupa diversas vantagens de cada abordagem e oferece resultados mais estáveis. 

-----------------------

## Execuções e Resultados

### Casos de teste
Foram selecionados 4 casos de teste distintos, com diferentes graus de dificuldade, tendo-se regiões de interesse com características que abrangem casos simples, com formatos mais uniformes, e casos mais desafiadores, em regiões limítrofes e formas complexas. Os mesmos casos de teste foram aplicados em ambos os métodos de segmentação. Cada caso possui entre 6 a 9 slices em cada, juntamente totalizando 31 slices.

Um _slice_ de referência foi selecionado para cada caso de teste. A partir desse _slice_, técnicas de pré-processamento (quando necessário) e respectivos parâmetros, tanto das técnicas de pré-processamento quanto dos métodos de segmentação, foram ajustados para se obter uma segmentação satisfatória. Para o caso específico do método Watershed, esta etapa também inclui a definição da semente localizada na região de interesse.

A ideia é que, obtendo-se uma boa segmentação para um _slice_ especifico, que os mesmos procedimentos e parâmetros possam ser executados em slices anteriores ou posteriores que também contenham a lesão de interesse. Desta forma, estima-se que possa ser automatizada uma segmentação em _batch_ da mesma lesão a medida que se manifesta em diversos _slices_.

Os casos são definidos no arquivo `args_test.py`, contendo todas as informações necessárias para sua reprodução automática para a execução e avaliação deste projeto. 

Os casos de testes podem ser executados por meio dos notebooks apresentados a seguir para ambos os métodos de segmentação, bem como por meio da execução do arquivo `run_segmentation.py` dentro do diretório `src`. Neste último, a execução esta definida para executar ambos os métodos de segmentação para cada um dos casos de teste. O processo pode ser demorado. Arquivos com as figuras do mosaico de gráficos são gravados no diretório `src` ao longo da execução para facilitar a visualização dos resultados.

### Resultados
Nesta seção são apresentados as análises e resultados detalhados de ambos os métodos, com os passos de execução necessários. Ainda, é apresentada uma análise comparativa, avaliada quantitivamente e qualititivamente, entre ambos os métodos.

#### Execução e resultados para a segmentação Chan-Vese
Devido a extensão das análises, para fins de organização as execuções e resultados são descritos separadamente no [notebook de Casos de teste com Chan-Vese](notebooks/Analise_Casos_Chan_Vese.ipynb)

#### Execução e resultados para a segmentação Watershed
Devido a extensão das análises, para fins de organização as execuções e resultados são descritos separadamente no [notebook de Casos de teste com Watershed](notebooks/Analise_Casos_Watershed.ipynb)

#### Avaliação comparativa entre Watershed e Chan-Vese
Devido a extensão das análises, para fins de organização as execuções e resultados são descritos separadamente no [notebook de Análise comparativa Watershed e Chan-Vese](notebooks/Analise_Comparativa_Conjunta.ipynb)

### Discussão e Conclusões
Os métodos de segmentação apresentados tiveram resultados complementares em diversos casos, com vantagens e desvantagens específicas. Em alguns segmentos, o método watershed obteve maior precisão e fidedignidade a máscara _groundtruth_, principalmente nos casos onde formas eram complexas e possuíam estrutura mais pontiaguda e não arredondada. Contudo, em diversos outros casos, o método Watershed falhou em obter até mesmo alguma máscara significativa, ou apresentou grandes vazamentos para regiões adjacentes de não-interesse. Ainda, para uma execução bem-sucedida, passos de pré-processamento são necessários, o que em cenários reais requer conhecimento específico do operador humano e demanda tempo adicional para encontrar os parâmetros e procedimentos adequados, contudo sem garantir que estes procedimentos acabem por se mostrar efetivos para os demais _slices_, mesmo os imediatamente anteriores ou posteriores. 

O método Chan-Vese apresentou melhores médias nos índices _Dice_ de similaridade, quase sempre retornando alguma máscara em todos os casos e _slices_. Apesar de ter resultados com máscaras diversas vezes com formatos mais arredondados que o _groundtruth_, uma etapa de pós-processamento para refino dessas regiões por um agente humano poderia ser efetiva e não demasiadamente custosa. Ainda, apesar de um tempo de execução maior, o método Chan-Vese obteve resultados satisfatórios mesmo sem praticamente nenhuma etapa de pré-processamento, evitando o requisito de um operador humano com esse conhecimento e o tempo necessário dedicado a procura dos parâmetros adequados.

#### Atividades dos participantes
> **Iury Andrade:** Escrita do readme, seleção do conjunto de dados, desenvolvimentos dos processos do método watershed, participação no vídeo de apresentação do projeto

> **Rodrigo Duarte:** Escrita do Readme, desenvolvimentos dos processos do método Chan-Vese, participação do vídeo de apresentação do projeto

#### Referências

Pérez-García F., Rodionov R., Alim-Marvasti A., Sparks R., Duncan J.S., Ourselin S. (2020) Simulation of Brain Resection for Cavity Segmentation Using Self-supervised and Semi-supervised Learning. In: Martel A.L. et al. (eds) Medical Image Computing and Computer Assisted Intervention – MICCAI 2020. Lecture Notes in Computer Science, vol 12263. Springer, Cham. https://doi.org/10.1007/978-3-030-59716-0_12

Pérez-García F., Rodionov R., Alim-Marvasti A., Sparks R., Duncan J.S., Ourselin S. EPISURG: MRI dataset for quantitative analysis of resective neurosurgery for refractory epilepsy. University College London (2020). DOI 10.5522/04/9996158.v1

