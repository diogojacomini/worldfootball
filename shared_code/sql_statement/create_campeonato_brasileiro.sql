CREATE TABLE campeonato_brasileiro (
    Posicao INT,
    Time VARCHAR(255),
    Rodada INT,
    Vitoria INT,
    Empate INT,
    Derrota INT,
    Gols INT,
    GolsSofridos INT,
    DiferencaGols INT,
    Pontos INT,
    Temporada INT,
    CONSTRAINT uc_campeonato_brasileiro UNIQUE (Time, Rodada, Temporada)
);
