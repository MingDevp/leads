import logging

from sqlmodel import SQLModel

from deps import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Creating initial data")
    SQLModel.metadata.create_all(engine)
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
