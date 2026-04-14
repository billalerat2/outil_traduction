from sacrebleu import corpus_bleu, corpus_chrf


class Evaluator:
    """
    Evalue la qualite des traductions a l'aide de metriques standard :
    - BLEU
    - chrF
    """

    def __init__(self, df, reference_col="reference", hypothesis_col="translation"):
        self.references = df[reference_col].tolist()
        self.hypotheses = df[hypothesis_col].tolist()

    def compute_bleu(self):
        bleu = corpus_bleu(self.hypotheses, [self.references])
        return bleu.score

    def compute_chrf(self):
        chrf = corpus_chrf(self.hypotheses, [self.references])
        return chrf.score

    def evaluate(self):
        return {"BLEU": self.compute_bleu(), "chrF": self.compute_chrf()}
