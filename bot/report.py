

def create_markdown_report(user_data, report_data):
    """Формирует отчет в формате Markdown из данных о пользователе и данных отчета."""
    report_text = f"# Отчет по спринту {report_data['sprint_number']}\n\n"

    report_text += f"## Сотрудник: {user_data['first_name']} {user_data['last_name']}\n\n"

    report_text += f"### Отчет:\n\n{report_data['report_text']}\n\n"

    return report_text