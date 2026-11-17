"""Independent checks for the synthetic Study Space Challenge (stdlib only)."""
import unittest
from model import load_csv, distance, nearest, validate_row, report

class PracticeProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.train=load_csv("train.csv")
        cls.validation=load_csv("validation.csv")
        cls.test=load_csv("test.csv")

    def test_complete_disjoint_splits(self):
        rows=self.train+self.validation+self.test
        self.assertEqual((len(self.train),len(self.validation),len(self.test)),(150,45,45))
        self.assertEqual(len({r["id"] for r in rows}),240)
        self.assertEqual(len({tuple(r[f] for f in ("occupancy","noise","wifi","outlets","minutes")) for r in rows}),240)
        for row in rows: validate_row(row)

    def test_distance_symmetry(self):
        a=self.train[0];b=self.train[1]
        self.assertAlmostEqual(distance(a,b),distance(b,a))
        self.assertEqual(distance(a,a),0.0)

    def test_valid_prediction_and_trace(self):
        sample={"occupancy":35,"noise":40,"wifi":4,"outlets":1,"minutes":60}
        prediction,trace=nearest(self.train,sample,1)
        self.assertEqual(prediction,"good")
        self.assertEqual(len(trace),1)
        self.assertEqual(trace[0][1],"good")

    def test_invalid_input_rejected(self):
        sample={"occupancy":35,"noise":40,"wifi":8,"outlets":1,"minutes":60}
        with self.assertRaisesRegex(ValueError,"Out-of-range wifi"):
            nearest(self.train,sample,3)

    def test_locked_reference_scores(self):
        results=report(self.train,self.validation,self.test)
        self.assertEqual(results["baseline_label"],"avoid")
        self.assertEqual(results["baseline_validation"],15)
        self.assertEqual(results["scores"],{1:41,3:39,5:39,7:41})
        self.assertEqual(results["chosen_k"],1)
        self.assertEqual(results["test"]["correct"],38)
        self.assertEqual(results["test"]["total"],45)

if __name__=="__main__":
    unittest.main(verbosity=2)
