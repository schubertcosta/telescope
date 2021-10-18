clear all;
clc;

// RRP Esférico
// ----Parâmetros Iniciais----
l1 = 0.5;
l2 = 0.4;

//moduloAceleracao = 0.1; % modulo da aceleração p/ quinta ordem
//tempoTotalSegmento = 12; % tempo em segundos
//taxaAmostragem = 0.1; %taxa de amostragem
//fatorDePrecisao = 0.001; %Precisao do movimento em metros
//angulos(1,:) = [0 0 0]; % posicao inicial do braço robótico
//r = 0.2; % raio da circunferencia
//fatorConversao = pi/180;

//Seleciona o tipo de parametrização desejada, 'cubica', 'quinta_ordem' ou
//'reta_parabola'
//[matrizPosicao, matrizVelocidade, matrizAceleracao, qtdPontos] = selecionaParametrizacao('cubica', tempoTotalSegmento, taxaAmostragem, moduloAceleracao);

//%---- Cinemática da posicação---%
//%----Variáveis Simbólicas----%
Syms q1 q2;
q = [q1 q2];

//%----Entrando com as matrizes de rotação e translação----%
//%---Para resolver os problemas de q1,q2 e q3---%
R10 = rotacionaMatriz('z', q(1));
D10 = transladaMatriz([0 0 l1]);
T10 = R10*D10;

R21 = rotacionaMatriz('y', q(2));
D21 = transladaMatriz([l2 0 0]);
T21 = R21*D21;

T30sym = T10*T21;
