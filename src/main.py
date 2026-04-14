import os
from config import DATA_DIR, OUTPUT_DIR
from loaders.loader_factory import LoaderFactory
from processors.data_processor import DataProcessor
from translators.translator import Translator
from evaluators.evaluator import Evaluator


def main():
    """
    Fonction principale d'orchestration du pipeline de traduction.
    """

    # --- 1. Resolve input file path ---
    file_path = os.path.join(DATA_DIR, "sample02.json")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    # --- 2. Load data ---
    loader = LoaderFactory.create(file_path)
    df = loader.to_dataframe()
    print(f"Loaded {len(df)} rows.")

    # --- 3. Clean/process data ---
    processor = DataProcessor(df)
    df = processor.clean()

    # --- 4. Translate ---
    translator = Translator("Helsinki-NLP/opus-mt-fr-en")
    df = translator.translate(df, column="source", new_column="translation")

    # --- 5. Prepare output path ---
    if not os.path.isdir(OUTPUT_DIR):
        raise RuntimeError(f"Output directory does not exist: {OUTPUT_DIR}")

    output_path = os.path.join(OUTPUT_DIR, "translated.csv")

    # --- 6. Save results ---
    df.to_csv(output_path, index=False)
    print(f"Saved translated file to: {output_path}")

    # --- 7. Evaluate translation quality ---
    evaluator = Evaluator(df)
    scores = evaluator.evaluate()

    print("\nTranslation quality metrics:")
    for metric, value in scores.items():
        print(f"  {metric}: {value:.2f}")


if __name__ == "__main__":
    main()
