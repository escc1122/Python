import db
import model

if __name__ == '__main__':
    engine = db.get_engine()
    model.Base.metadata.create_all(engine)


