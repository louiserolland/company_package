# company/medical/medical.py
from importlib.resources import files
import pandas as pd
from ..base_company import Company

class MedicalCompany(Company):
    # pass
    def __init__(self, name, specialty, drug_manufacturer=False, ticker=None):
        """
        Initialize a MedicalCompany instance.

        Parameters:
        - name (str): Name of the company.
        - specialty (str): Medical specialty (e.g., "Cardiology", "Oncology").
        - drug_manufacturer (bool): Indicates if the company manufactures drugs.
        - ticker (str): Stock ticker symbol if the company is available on yfinance.
        """
        super().__init__(name, ticker)
        self.specialty = specialty
        self.drug_manufacturer = drug_manufacturer

    def display_info(self):
        """Displays basic information about the medical company."""
        super().display_info()
        print(f"Medical Specialty: {self.specialty}")
        print(f"Drug Manufacturer: {'Yes' if self.drug_manufacturer else 'No'}")

    def drug_approval_summary(self, dataset_path=None):
        """
        Prints a summary of drug approval attempts for the company's drugs.
        
        Parameters:
        - dataset_path (str): Path to the dataset with drug approval data.
          If not provided, uses the default package data file.

        Example:
            >>> medical_company = MedicalCompany("Pfizer", "Pharmaceuticals", drug_manufacturer=True)
            >>> medical_company.drug_approval_summary()
            
            Drug Approval Summary for Pfizer:
             - Drug A: 2 failed attempt(s) before approval
             - Drug B: 0 failed attempt(s) before approval
             - Drug C: 1 failed attempt(s) before approval
        """
        if not self.drug_manufacturer:
            print(f"{self.name} is not involved in drug manufacturing.")
            return

        # Use default dataset if no path is provided
        if not dataset_path:
            dataset_path = files("company").joinpath("data/drug_data.csv")

        try:
            # Load dataset
            data = pd.read_csv(dataset_path)
            
            # Filter data for this company's drugs
            company_data = data[data["company_name"] == self.name]
            
            # Summarize approval attempts
            summary = company_data.groupby("drug_name")["approval_attempts"].max() - 1

            print(f"\nDrug Approval Summary for {self.name}:")
            for drug, attempts in summary.items():
                print(f" - {drug}: {attempts} failed attempt(s) before approval")
        
        except FileNotFoundError:
            print(f"Dataset file {dataset_path} not found.")
        except Exception as e:
            print(f"An error occurred while processing the dataset: {e}")
