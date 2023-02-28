import requests
import argparse

MALWR_API_KEY = "your-malwr-api-key"

def analyze_file(file_path):
    url = "https://malwr.com/api/v1/analysis/create/"
    headers = {"Authorization": "api_key {}".format(MALWR_API_KEY)}
    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            analysis_id = response.json().get("analysis_id")
            return analysis_id
        else:
            return None

def check_analysis_status(analysis_id):
    url = "https://malwr.com/api/v1/analysis/status/{}".format(analysis_id)
    headers = {"Authorization": "api_key {}".format(MALWR_API_KEY)}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        status = response.json().get("status")
        return status
    else:
        return None

def get_analysis_report(analysis_id):
    url = "https://malwr.com/api/v1/analysis/get/{}".format(analysis_id)
    headers = {"Authorization": "api_key {}".format(MALWR_API_KEY)}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        report = response.json()
        return report
    else:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a malware file using the malwr.com API")
    parser.add_argument("file", type=str, help="Path to the malware file")
    args = parser.parse_args()

    analysis_id = analyze_file(args.file)
    if analysis_id:
        print("Analysis submitted. ID: {}".format(analysis_id))
        while True:
            status = check_analysis_status(analysis_id)
            if status == "SUCCESS":
                print("Analysis complete.")
                report = get_analysis_report(analysis_id)
                if report:
                    print("Report retrieved.")
                    # do something with the report
                    break
                else:
                    print("Report retrieval failed.")
                    break
            elif status == "FAILURE":
                print("Analysis failed.")
                break
            else:
                print("Analysis status: {}".format(status))
    else:
        print("Analysis submission failed.")
