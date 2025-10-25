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
    url varchar(100) unique key not null,
    nome varchar(90),
    descricao varchar(150),
    id_usuario bigint,
    foreign key (id_usuario) references Usuario(id)
);


create table Usuario_Dataset(
	id_usuario bigint,
    id_dataset bigint,
    foreign key (id_usuario) references Usuario(id),
    foreign key (id_dataset) references Dataset(id)
);


