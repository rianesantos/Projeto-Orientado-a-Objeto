import requests
import json
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.box import ROUNDED

console = Console()
BASE_URL = "http://127.0.0.1:8000"
AUTH_TOKEN = None

def clear_screen():
    console.clear()
    
def handle_request(method, url, data=None, headers=None):
    try:
        response = requests.request(method, url, json=data, headers=headers)
        response.raise_for_status()
        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            console.print("[yellow]Warning: Response is not JSON[/yellow]")
            return {"raw_text": response.text}

    except requests.exceptions.HTTPError as e:
        error_msg = None
        try:
            error_msg = e.response.json().get('detail', 'Unknown error')
        except Exception:
            error_msg = e.response.text  # pega texto cru caso não seja JSON
        console.print(f"[red]HTTP Error: {e.response.status_code} - {error_msg}[/red]")
        return None
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Request Error: {e}[/red]")
        console.print("[yellow]Please make sure your backend server is running.[/yellow]")
        return None

def auth_required(func):
    def wrapper(*args, **kwargs):
        if not AUTH_TOKEN:
            console.print("[red]Authentication required. Please log in first.[/red]")
            return
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        return func(*args, **kwargs, headers=headers)
    return wrapper

# --- Authentication and Main Logic ---

def login_user():
    global AUTH_TOKEN
    console.print(Panel("[bold cyan]Login[/bold cyan]"))
    email = Prompt.ask("Enter your email")
    password = Prompt.ask("Enter your password", password=True)

    payload = {"username": email, "password": password}
    response = handle_request("POST", f"{BASE_URL}/auth/token", data=payload)
    if response and "access_token" in response:
        AUTH_TOKEN = response["access_token"]
        console.print("[bold green]Login successful![/bold green]")
        return True
    return False

def register_user():
    console.print(Panel("[bold cyan]Register[/bold cyan]"))
    email = Prompt.ask("Enter your email")
    password = Prompt.ask("Enter your password", password=True)
    username = Prompt.ask("Enter your username")

    payload = {"email": email, "password": password, "username": username}
    response = handle_request("POST", f"{BASE_URL}/auth/register", data=payload)
    if response:
        console.print("[bold green]Registration successful. Please log in.[/bold green]")
        return True
    return False

def check_auth_status():
    global AUTH_TOKEN
    if not AUTH_TOKEN:
        return False
    
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    response = handle_request("GET", f"{BASE_URL}/users/me", headers=headers)
    if response:
        console.print(f"[bold green]Authenticated as {response.get('email')}[/bold green]")
        return True
    
    AUTH_TOKEN = None
    return False

def auth_screen():
    while True:
        clear_screen()
        console.print(Panel("[bold green]Welcome to the Trading System[/bold green]", expand=False, box=ROUNDED))
        choice = Prompt.ask("Choose an option", choices=["Login", "Register", "Exit"])
        
        if choice == "Login":
            if login_user():
                break
        elif choice == "Register":
            register_user()
        elif choice == "Exit":
            console.print("[bold cyan]Exiting...[/bold cyan]")
            return False
        
        Prompt.ask("Press Enter to continue...")
    return True

# --- Main Menu Functions ---

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
    if response:
        console.print("[bold green]Strategy created successfully![/bold green]")
        console.print(response)

@auth_required
def edit_strategy(headers):
    list_strategies(headers)
    console.print(Panel("[bold green]Edit Strategy[/bold green]"))
    try:
        strategy_id = int(Prompt.ask("Enter the ID of the strategy to edit"))
        name = Prompt.ask("Enter the new name (leave blank to skip)")
        description = Prompt.ask("Enter the new description (leave blank to skip)")
        
        payload = {}
        if name: payload['name'] = name
        if description: payload['description'] = description

        if not payload:
            console.print("[yellow]No changes detected.[/yellow]")
            return
            
        response = handle_request("PUT", f"{BASE_URL}/strategies/{strategy_id}", data=payload, headers=headers)
        if response:
            console.print("[bold green]Strategy updated successfully![/bold green]")
            console.print(response)
        
    except ValueError:
        console.print("[red]Invalid ID. Please enter a number.[/red]")

@auth_required
def delete_strategy(headers):
    list_strategies(headers)
    console.print(Panel("[bold red]Delete Strategy[/bold red]"))
    try:
        strategy_id = int(Prompt.ask("Enter the ID of the strategy to delete"))
        if Confirm.ask("Are you sure you want to delete this strategy?"):
            response = handle_request("DELETE", f"{BASE_URL}/strategies/{strategy_id}", headers=headers)
            if response:
                 console.print("[bold green]Strategy deleted successfully![/bold green]")
        
    except ValueError:
        console.print("[red]Invalid ID. Please enter a number.[/red]")

@auth_required
def manage_portfolio(headers):
    console.print(Panel("[bold green]Manage Portfolio[/bold green]"))
    console.print("[yellow]This functionality is not yet implemented on the API.[/yellow]")

@auth_required
def run_backtest(headers):
    console.print(Panel("[bold green]Run Backtest[/bold green]"))
    console.print("[yellow]This functionality is not yet implemented on the API.[/yellow]")

@auth_required
def view_notifications(headers):
    console.print(Panel("[bold green]View Notifications[/bold green]"))
    console.print("[yellow]This functionality is not yet implemented on the API.[/yellow]")

@auth_required
def analyze_market_data(headers):
    console.print(Panel("[bold green]Analyze Market Data[/bold green]"))
    console.print("[yellow]This functionality is not yet implemented on the API.[/yellow]")

@auth_required
def manage_risk(headers):
    console.print(Panel("[bold green]Risk Management Tools[/bold green]"))
    console.print("[yellow]This functionality is not yet implemented on the API.[/yellow]")

@auth_required
def view_reports(headers):
    console.print(Panel("[bold green]Reports and Analytics[/bold green]"))
    console.print("[yellow]This functionality is not yet implemented on the API.[/yellow]")

def main_loop():
    if not auth_screen():
        return

    while True:
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
            manage_portfolio(None) # These functions don't need the header yet
        elif choice == '6':
            run_backtest(None)
        elif choice == '7':
            view_notifications(None)
        elif choice == '8':
            analyze_market_data(None)
        elif choice == '9':
            manage_risk(None)
        elif choice == '10':
            view_reports(None)
        elif choice == '11':
            console.print("[bold cyan]Logging out and exiting...[/bold cyan]")
            break
            
        Prompt.ask("[dim]Press Enter to continue...[/dim]")

if __name__ == "__main__":
    main_loop()