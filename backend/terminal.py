import requests
import functools
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.box import ROUNDED

console = Console()
BASE_URL = "http://127.0.0.1:8000"
AUTH_TOKEN = None
TOKEN_TYPE = "Bearer"

def clear_screen():
    console.clear()

def handle_request(method, url, data=None, headers=None, as_json=True):
    try:
        if as_json:
            response = requests.request(method, url, json=data, headers=headers)
        else:
            response = requests.request(method, url, data=data, headers=headers)
        response.raise_for_status()
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"raw_text": response.text}
    except requests.exceptions.HTTPError as e:
        try:
            error_msg = e.response.json().get('detail', 'Unknown error')
        except Exception:
            error_msg = e.response.text
        console.print(f"[red]HTTP Error: {e.response.status_code} - {error_msg}[/red]")
        return None
    except requests.exceptions.ConnectionError:
        console.print("[red]Error: Cannot connect to server. Make sure the backend is running on http://127.0.0.1:8000[/red]")
        return None
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Request Error: {e}[/red]")
        return None

def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global AUTH_TOKEN, TOKEN_TYPE
        if not AUTH_TOKEN:
            console.print("[red]Authentication required. Please log in first.[/red]")
            return
        headers = {
            "Authorization": f"{TOKEN_TYPE.capitalize()} {AUTH_TOKEN}",
            "Content-Type": "application/json",
        }
        kwargs['headers'] = headers
        return func(*args, **kwargs)
    return wrapper

def login_user():
    global AUTH_TOKEN, TOKEN_TYPE
    username = Prompt.ask("Enter your username")
    password = Prompt.ask("Enter your password", password=True)
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data={"username": username, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            data = response.json()
            AUTH_TOKEN = data["access_token"]
            TOKEN_TYPE = data.get("token_type", "bearer")
            console.print("[bold green]Login successful![/bold green]")
            return True
        else:
            try:
                error_detail = response.json().get('detail', response.text)
            except:
                error_detail = response.text
            console.print(f"[bold red]Login failed: {error_detail}[/bold red]")
            return False
            
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Error: Cannot connect to server. Make sure the backend is running on http://127.0.0.1:8000[/bold red]")
        return False
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {e}[/bold red]")
        return False

def register_user():
    console.print(Panel("[bold cyan]Register[/bold cyan]"))
    email = Prompt.ask("Enter your email")
    username = Prompt.ask("Enter your username")
    password = Prompt.ask("Enter your password", password=True)
    payload = {"email": email, "username": username, "password": password}
    response = handle_request("POST", f"{BASE_URL}/auth/register", data=payload)
    if response:
        console.print("[bold green]Registration successful. Please log in.[/bold green]")
        return True
    return False

def auth_screen():
    while True:
        clear_screen()
        console.print(Panel("[bold green]Welcome to the Trading System[/bold green]", expand=False, box=ROUNDED))
        choice = Prompt.ask("Choose an option", choices=["Login", "Register", "Exit"])
        if choice == "Login":
            if login_user(): break
        elif choice == "Register":
            register_user()
        elif choice == "Exit":
            console.print("[bold cyan]Exiting...[/bold cyan]")
            return False
        Prompt.ask("Press Enter to continue...")
    return True

def display_menu():
    clear_screen()
    console.print(Panel("[bold green]Main Menu[/bold green]", expand=False, box=ROUNDED))
    table = Table(title="Functionalities", style="dim")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_row("1", "List Strategies")
    table.add_row("2", "Create New Strategy")
    table.add_row("3", "Edit Strategy")
    table.add_row("4", "Delete Strategy")
    table.add_row("5", "Manage Portfolio")
    table.add_row("6", "Run Backtest")
    table.add_row("7", "View Notifications")
    table.add_row("8", "Analyze Market Data")
    table.add_row("9", "Risk Management Tools")
    table.add_row("10", "Reports and Analytics")
    table.add_row("11", "Logout")
    console.print(table)

@auth_required
def list_strategies(headers):
    strategies = handle_request("GET", f"{BASE_URL}/strategies/", headers=headers)
    if strategies is None: return
    if not strategies:
        console.print("[yellow]No strategies found.[/yellow]")
        return
    table = Table(title="Current Strategies", style="dim")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Description", style="white")
    table.add_column("Active?", style="magenta")
    for s in strategies:
        active_status = "[green]Yes[/green]" if s.get('is_active') else "[red]No[/red]"
        table.add_row(str(s.get('id')), s.get('name'), s.get('description'), active_status)
    console.print(table)

@auth_required
def create_strategy(headers):
    console.print(Panel("[bold green]Create New Strategy[/bold green]"))
    name = Prompt.ask("Enter strategy name")
    description = Prompt.ask("Enter strategy description")
    payload = {"name": name, "description": description, "is_active": False}
    response = handle_request("POST", f"{BASE_URL}/strategies/", data=payload, headers=headers)
    if response: console.print("[bold green]Strategy created successfully![/bold green]")

@auth_required
def edit_strategy(headers):
    list_strategies(headers)
    if not AUTH_TOKEN:  
        return
    strategy_id = Prompt.ask("Enter the ID of the strategy to edit")
    name = Prompt.ask("Enter new name (blank to skip)")
    description = Prompt.ask("Enter new description (blank to skip)")
    payload = {}
    if name.strip(): payload['name'] = name
    if description.strip(): payload['description'] = description
    if not payload: 
        console.print("[yellow]No changes detected.[/yellow]")
        return
    response = handle_request("PUT", f"{BASE_URL}/strategies/{strategy_id}", data=payload, headers=headers)
    if response: console.print("[bold green]Strategy updated successfully![/bold green]")

@auth_required
def delete_strategy(headers):
    list_strategies(headers)
    if not AUTH_TOKEN:  
        return
    strategy_id = Prompt.ask("Enter the ID of the strategy to delete")
    if Confirm.ask("Are you sure you want to delete this strategy?"):
        response = handle_request("DELETE", f"{BASE_URL}/strategies/{strategy_id}", headers=headers)
        if response: console.print("[bold green]Strategy deleted successfully![/bold green]")

@auth_required
def manage_portfolio(headers):
    while True:
        clear_screen()
        console.print(Panel("[bold green]Portfolio Management[/bold green]", expand=False, box=ROUNDED))
        table = Table(title="Portfolio Options", style="dim")
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")

        table.add_row("1", "View Portfolio")
        table.add_row("2", "Add Asset")
        table.add_row("3", "Calculate Total Value")
        table.add_row("4", "Back to Main Menu")

        console.print(table)

        choice = Prompt.ask("[bold]Choose an option[/bold]", choices=["1", "2", "3", "4"])

        if choice == "1":
            response = handle_request("GET", f"{BASE_URL}/portfolios/", headers=headers)
            if response is not None:
                if len(response) == 0:
                    console.print("[yellow]Your portfolio is empty.[/yellow]")
                else:
                    table = Table(title="Current Portfolio", style="dim")
                    table.add_column("Asset", style="cyan")
                    table.add_column("Quantity", style="green")
                    table.add_column("Average Price", style="white")
                    for p in response:
                        table.add_row(p["asset"], str(p["quantity"]), str(p["avg_price"]))
                    console.print(table)

        elif choice == "2":
            try:
                symbol = Prompt.ask("Enter asset symbol (e.g. AAPL, PETR4)")
                quantity = float(Prompt.ask("Enter quantity"))
                price = float(Prompt.ask("Enter purchase price"))

                payload = {"asset": symbol, "quantity": quantity, "avg_price": price}
                response = handle_request("POST", f"{BASE_URL}/portfolios/", data=payload, headers=headers)
                if response:
                    console.print("[bold green]Asset added successfully![/bold green]")
            except ValueError:
                console.print("[bold red]Invalid number format. Please try again.[/bold red]")

        elif choice == "3":
            response = handle_request("GET", f"{BASE_URL}/portfolios/", headers=headers)
            if response:
                total_value = sum(p["quantity"] * p["avg_price"] for p in response)
                console.print(f"[bold cyan]Total Portfolio Value: ${total_value:.2f}[/bold cyan]")

        elif choice == "4":
            break

        Prompt.ask("[dim]Press Enter to continue...[/dim]")

@auth_required
def run_backtest(headers):
    try:
        strategy_id = int(Prompt.ask("Enter strategy ID to run backtest"))
        payload = {"strategy_id": strategy_id}
        response = handle_request("POST", f"{BASE_URL}/backtest/", data=payload, headers=headers)
        if response:
            console.print(f"[bold green]Backtest Results:[/bold green]\n"
                          f"Trades Executed: {response.get('trades_executed', 'N/A')}\n"
                          f"Profit/Loss: ${response.get('profit_loss', 'N/A')}\n"
                          f"Success Rate: {response.get('success_rate', 0)*100:.2f}%")
    except ValueError:
        console.print("[bold red]Invalid strategy ID. Please enter a number.[/bold red]")

@auth_required
def view_notifications(headers):
    response = handle_request("GET", f"{BASE_URL}/alerts/", headers=headers)
    if response is not None:
        if not response:
            console.print("[yellow]No notifications found.[/yellow]")
            return
        table = Table(title="Notifications", style="dim")
        table.add_column("ID", style="cyan")
        table.add_column("Message", style="white")
        for alert in response:
            table.add_row(str(alert.get("id", "N/A")), alert.get("message", "N/A"))
        console.print(table)

@auth_required
def analyze_market_data(headers):
    ticker = Prompt.ask("Enter asset ticker (e.g. AAPL, PETR4)")
    response = handle_request("GET", f"{BASE_URL}/market/{ticker}", headers=headers)
    if response:
        price = response.get('price', 'N/A')
        console.print(f"[bold green]{ticker.upper()} Current Price:[/bold green] ${price}")

@auth_required
def manage_risk(headers):
    response = handle_request("GET", f"{BASE_URL}/risk/", headers=headers)
    if response:
        console.print(f"[bold green]Risk Metrics:[/bold green]\n"
                      f"Max Exposure: ${response.get('max_exposure', 'N/A')}\n"
                      f"Current Exposure: ${response.get('current_exposure', 'N/A')}\n"
                      f"Risk Level: {response.get('risk_level', 'N/A')}")

@auth_required
def view_reports(headers):
    response = handle_request("GET", f"{BASE_URL}/reports/", headers=headers)
    if response is not None:
        if not response:
            console.print("[yellow]No reports found.[/yellow]")
            return
        table = Table(title="Reports", style="dim")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Summary", style="white")
        for r in response:
            table.add_row(
                str(r.get("id", "N/A")), 
                r.get("title", "N/A"), 
                r.get("summary", "N/A")
            )
        console.print(table)

def main_loop():
    if not auth_screen(): 
        return
    
    while True:
        try:
            display_menu()
            choice = Prompt.ask("[bold]Choose an option[/bold]", choices=[str(i) for i in range(1, 12)])
            clear_screen()
            
            if choice == '1': 
                list_strategies()
            elif choice == '2': 
                create_strategy()
            elif choice == '3': 
                edit_strategy()
            elif choice == '4': 
                delete_strategy()
            elif choice == '5': 
                manage_portfolio()
            elif choice == '6': 
                run_backtest()
            elif choice == '7': 
                view_notifications()
            elif choice == '8': 
                analyze_market_data()
            elif choice == '9': 
                manage_risk()
            elif choice == '10': 
                view_reports()
            elif choice == '11':
                global AUTH_TOKEN
                AUTH_TOKEN = None
                console.print("[bold cyan]Logging out and exiting...[/bold cyan]")
                break
                
            Prompt.ask("[dim]Press Enter to continue...[/dim]")
            
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Operation cancelled by user.[/bold yellow]")
            if Confirm.ask("Do you want to exit?"):
                break
        except Exception as e:
            console.print(f"[bold red]Unexpected error: {e}[/bold red]")
            Prompt.ask("[dim]Press Enter to continue...[/dim]")

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        console.print("\n[bold cyan]Goodbye![/bold cyan]")
    except Exception as e:
        console.print(f"[bold red]Fatal error: {e}[/bold red]")
