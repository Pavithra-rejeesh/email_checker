from disposable_email_detector_pro import assess_email

test_cases = [
    # (email, is_disposable?)
    ("test@10minutemail.com", True),
    ("fake@mailinator.com", True),
    ("random@guerrillamail.com", True),
    ("abc123@tempmail.net", True),
    ("user@gmail.com", False),
    ("person@yahoo.com", False),
    ("john.doe@outlook.com", False),
    ("admin@company.com", False),
]

correct = 0

print("=" * 50)
print(f"{'Email':<35} {'Expected':<12} {'Got':<8} {'✓/✗'}")
print("=" * 50)

for email, expected in test_cases:
    result = assess_email(email)
    predicted = result["action"] == "BLOCK"
    is_correct = predicted == expected

    if is_correct:
        correct += 1

    status = "✅" if is_correct else "❌"
    print(f"{email:<35} {'BLOCK' if expected else 'ALLOW':<12} {result['action']:<8} {status}")

print("=" * 50)
accuracy = correct / len(test_cases)
print(f"Accuracy: {correct}/{len(test_cases)} = {accuracy * 100:.1f}%")