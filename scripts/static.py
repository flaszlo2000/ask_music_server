from scripts.shared.ws.connection_manager import WSConnectionManager

#! NOTE: here I define static object that I want to share between multiple modules

#region NOTE: lifecycle is handled at main.py and used to create ws connection in admin.py
ws_connection_manager = WSConnectionManager() 
#endregion