from sqlmodel import Field, SQLModel


class Exporta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pais: str = Field(index=True, max_length=50)
    tipo: str = Field(max_length=50)
    ano: int
    quantidade: int | None = Field(default=0)
    valor: int | None = Field(default=None)


class Importa(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pais: str = Field(index=True, max_length=50)
    tipo: str = Field(max_length=50)
    ano: int
    quantidade: int | None = Field(default=0)
    valor: int | None = Field(default=None)


class Producao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str
    produto: str = Field(index=True)
    ano: int
    quantidade: int | None = Field(default=0)


class Comercio(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str
    produto: str = Field(index=True)
    ano: int
    quantidade: int | None = Field(default=0)


class Processamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    control: str
    cultivar: str = Field(index=True)
    tipo: str
    ano: int
    quantidade: int | None = Field(default=None)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, max_length=50)
    hashed_password: str