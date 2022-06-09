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


!["Imagem exempo de IRM cerebral de região com região extraída, sem mascara de segmentação"](/ImgSemMascara.png "Imagem exempo de IRM cerebral de região com região extraída, sem mascara de segmentação") 

(a) Imagem exemplo de IRM cerebral de região extraída por meio de intervenção cirúrgica, sem máscara de segmentação


!["Imagem exempo de IRM cerebral de região com região extraídae com mascara de segmentação"](/ImgComMascara.png "Imagem exempo de IRM cerebral de região com região extraídae com mascara de segmentação")

(b) Imagem exemplo de IRM cerebral de região com região extraída e com máscara de segmentação

Figura 1 - Exemplo de imagens utilizadas para o procedimento. Fonte: [EPISURG dataset](https://rdr.ucl.ac.uk/articles/dataset/EPISURG_a_dataset_of_postoperative_magnetic_resonance_images_MRI_for_quantitative_analysis_of_resection_neurosurgery_for_refractory_epilepsy/9996158/1)