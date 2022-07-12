% importação de listing 
:- use_module(library(listing)).

% todos os ramos SIM (esquerda)
:- dynamic pergunta_s/2.
% todas as folhas SIM (esquerda)
:- dynamic animal_s/2.
% todos os ramos NAO (direita)
:- dynamic pergunta_n/2.
% todos as folhas NAO (direita)
:- dynamic animal_n/2.
:- dynamic root/1.

% Recebe o nó em questão e a resposta do jogador
analyse(Node,Answer):-
    write(Node),
    nl,
    read(Answer),
    nl,
    (
        (Answer=s,nl);
        (Answer=n,nl)
    ).
% percorre arvore de acordo com as respostas
whichnode(Node,Next):-
    write(Node),
    nl,
    read(Answer),
    nl,
    (
        (Answer=s,pergunta_s(Node,NextNode),whichnode(NextNode,Next),!);
        (Answer=s,not(pergunta_s(Node,_)),animal_s(Node,Next),!);
        (Answer=n,pergunta_n(Node,NextNode),whichnode(NextNode,Next),!);
        (Answer=n,not(pergunta_n(Node,_)),animal_n(Node,Next),!)
    ).


% add novo animal a arvore

% salva a base  de dados do jogo
salvar_base:-
	
	tell('Perguntas.txt'),
	listing([root,pergunta_s,animal_s,pergunta_n,animal_n]),
	told.

% aprende novos animais

learn(Current):-
    write("Qual animal pensou?"),
    nl,
    read(Animal),
    write("Qual pergunta devo fazer para distinguir os animais?"),
    nl,
    read(Question),
    write("Agora digite qual a resposta certa para "),
    write(Question),
    nl,
    read(YesNo),
    (
        (
        animal_s(Old,Current),
        retract(animal_s(Old,Current)),
        assertz(pergunta_s(Old,Question))
        );
        (
        animal_n(Old,Current),
        retract(animal_n(Old,Current)),
        assertz(pergunta_n(Old,Question))
        )
    ),
    (
        (YesNo=s,
        assertz(animal_s(Question,Animal)),
        assertz(animal_n(Question,Current))
        );
        (YesNo=n,
        assertz(animal_n(Question,Animal)),
        assertz(animal_s(Question,Current))
        )
    ).



% start game - consulta memória
start:- consult('Perguntas.txt').

run:- start,
    write("Bem-vindo ao jogo dos animais. Vou tentar adivinhar qual esta pensando"),
    nl,
    root(StartPoint),
    whichnode(StartPoint, Answer),
    analyse(Answer,Score),
    (
        (Score=s, write("YAY! Adivinhei seu animal!"),nl,nl);
        (Score=n,  write("Puxa! Eu nao sei!"),learn(Answer),nl,salvar_base)
    ).