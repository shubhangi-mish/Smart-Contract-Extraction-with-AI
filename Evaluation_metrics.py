import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

ground_truth = [
    {"field": "Contract ID", "value": "SOW-CFCU-WCOBCMC-2023"},
    {"field": "Customer Name", "value": "Company B"},
    {"field": "Contract Start Date", "value": "2023-12-13"},
    {"field": "Contract End Date", "value": "2026-12-13"},
    {"field": "Payment Terms", "value": "Upfront, Net 30"},
    {"field": "Contract Amount", "value": "$25,000"},
    {"field": "Billing Frequency", "value": "Monthly"},
    {"field": "Contract Type", "value": "Professional Services, Subscription Services"}
]

def extract_values_from_data(extracted_data):
    extracted_values = {}
    for field, field_data in extracted_data.items():
        if isinstance(field_data, dict):
            for nested_field, nested_data in field_data.items():
                if isinstance(nested_data, dict):
                    extracted_values[nested_field] = nested_data.get('extracted_value', '')
                else:
                    extracted_values[nested_field] = nested_data
        else:
            extracted_values[field] = field_data.get('extracted_value', '') if isinstance(field_data, dict) else field_data
    return extracted_values

def compare_fields(ground_truth, extracted_values):
    y_true = []
    y_pred = []

    truth_dict = {entry['field']: entry['value'] for entry in ground_truth}
    
    for field, extracted_value in extracted_values.items():
        if field in truth_dict:
            if truth_dict[field] == extracted_value:
                y_true.append(1)
                y_pred.append(1)
            else:
                y_true.append(1)
                y_pred.append(0)
        else:
            y_true.append(0)
            y_pred.append(0)
    
    return y_true, y_pred

def evaluate_extraction(extracted_data):
    extracted_values = extract_values_from_data(extracted_data)
    y_true, y_pred = compare_fields(ground_truth, extracted_values)

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    metrics = {
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy,
        "f1_score": f1
    }

    print("Extracted Values:")
    for field, value in extracted_values.items():
        print(f"{field}: {value}")

    print("\nEvaluation Metrics:")
    for metric, value in metrics.items():
        print(f"{metric.capitalize()}: {value:.2f}")

    metric_names = list(metrics.keys())
    metric_values = list(metrics.values())

    plt.figure(figsize=(10, 5))
    plt.bar(metric_names, metric_values, color=['blue', 'green', 'red', 'purple'])
    plt.xlabel('Metrics')
    plt.ylabel('Scores')
    plt.title('Evaluation Metrics')
    plt.ylim(0, 1)
    for i in range(len(metric_values)):
        plt.text(i, metric_values[i] / 2, f"{metric_values[i]:.2f}", ha='center', color='white', fontsize=12)
    plt.show()

    return metrics



