from pathlib import Path
from typing import Dict, List

import toml
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine


class Data(BaseModel):
    class PortalDestination(BaseModel):
        links: List[str]

    portal_desti: Dict[str, PortalDestination]


class PortalDestination(SQLModel, table=True):
    name: str = Field(primary_key=True)


class PortalDestinationLink(SQLModel, table=True):
    from_desti: str = Field(primary_key=True)
    to_desti: str = Field(primary_key=True)


with open(Path("./data.toml"), "r") as reader:
    data_string = reader.read()

data_toml = toml.loads(data_string)

data = Data(**data_toml)

sqlite_path = Path("cheesedata.db")
sqlite_url = f"sqlite:///{sqlite_path}"

engine = create_engine(sqlite_url)

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    for portal_desti_name, portal_desti_data in data.portal_desti.items():
        portal_destination = PortalDestination(name=portal_desti_name)
        session.add(portal_destination)

    for portal_desti_name, portal_desti_data in data.portal_desti.items():
        for portal_link_name in portal_desti_data.links:
            portal_link = PortalDestinationLink(from_desti=portal_desti_name, to_desti=portal_link_name)
            session.add(portal_link)

    session.commit()
