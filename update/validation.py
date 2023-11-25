from datetime import datetime, date


class ValidateData:
    def verify_start_and_end_dates(self, start_date: str, end_date: str) -> bool:
        """
        @author: Tarun https://github.com/tarundhurwe
        :method description: check whether the start date is prior to the end date
        """
        try:
            today = datetime.strptime(str(date.today()), "%Y-%m-%d")
            if start_date and end_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                if start_date < end_date <= today:
                    return True
                return "Start date cannot be greater than the end date. or dates cannot be greater than the today's date."
            elif start_date and not end_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                return (
                    True
                    if start_date <= today
                    else "Start date cannnot be future date."
                )
            return "Please provide valid start and end dates."
        except Exception as e:
            return f"Error: {e}"
