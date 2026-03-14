from py_db import db
import sys
from sklearn import linear_model
from py_fit_model import model_fitter


from py_db import db
db = db('nba_shots')


def process():
    entry = {}

    coefs = ["peak", "consistency", "premise", "plot",
    "information_gain", "desired_effects", "wit", "length",
    "timelessness"]

    qry = """SELECT
    adjustment AS 'target',
    peak, consistency, premise, plot,
    information_gain, desired_effects, wit, length,
    timelessness
    FROM _movies m
    """
    query = qry

    m = model_fitter("nba_shots",query,linear_model.LinearRegression(fit_intercept=False),"target",coefs)
    m.fit_model()

    entry = {"model_type":"movies"}
    for a,b in zip(coefs,m.model.coef_):
        entry["key"] = a
        entry["value"] = b
        print entry #####
        db.insertRowDict(entry,"_model_key_value",replace=True)
        db.conn.commit()


if __name__ == "__main__":
    process()
    
