create database WifiSensing;
use WifiSensing;

create table Usuario (
	id bigint auto_increment primary key,
    email varchar(80) unique key not null,
    nome varchar(90),
    senha varchar(16),
    permissao_usuario enum('1', '2', '3', '4') not null
);

create table Dispositivo (
	id bigint auto_increment primary key,
    nome varchar(90),
    descricao varchar(150),
    script_configuracao varchar(200)
);

create table Usuario_Dispositivo(
	id_usuario bigint,
    id_dispositivo bigint,
    foreign key (id_usuario) references Usuario(id),
    foreign key (id_dispositivo)  references Dispositivo(id)
);

create table Dataset(
	id bigint auto_increment primary key,
    url varchar(100) unique key not null,
    nome varchar(90),
    descricao varchar(150)
);

create table Modelo(
	id bigint primary key auto_increment,
    tipo enum('IA', 'Sistema') not null default 'IA',
    url varchar(120) unique key null,
    modelo longblob null,
    nome varchar(90),
    descricao varchar(150),
    descricao_algoritmo text null,
    parametros json null,
    id_usuario bigint,
    id_pai bigint null,
    foreign key (id_usuario) references Usuario(id) on delete cascade,
    foreign key (id_pai) references Modelo(id) on delete cascade
);

create table ItemModelo(
    id bigint primary key auto_increment,
    id_pai bigint not null,
    nome varchar(90) not null,
    descricao varchar(300),
    foreign key (id_pai) references Modelo(id) on delete cascade
);


create table Usuario_Dataset(
	id_usuario bigint,
    id_dataset bigint,
    foreign key (id_usuario) references Usuario(id),
    foreign key (id_dataset) references Dataset(id)
);


