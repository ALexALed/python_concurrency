import asyncio
import socket
 
from asynchronous_pizza_joint import Kitchen
 
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)
 
class Server:
    def __init__(self, event_loop: asyncio.AbstractEventLoop) -> None:
        self.event_loop = event_loop
        print(f"Starting up at: {ADDRESS}")
        self.server_socket = socket.create_server(ADDRESS)
        self.server_socket.setblocking(False)
 
    async def start(self) -> None: #A
        print("Server listening for incoming connections")
        try:
            while True:
                conn, client_address = await self.event_loop.sock_accept( #B
                    self.server_socket)
                self.event_loop.create_task(self.serve(conn))
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")
 
    async def serve(self, conn) -> None: #A
        while True:
            data = await self.event_loop.sock_recv(conn, BUFFER_SIZE)
            if not data:
                break
            try:
                order = int(data.decode())
                response = f"Thank you for ordering {order} pizzas!\n"
                print(f"Sending message to {conn.getpeername()}")
                await self.event_loop.sock_sendall( #B
                    conn, f"{response}".encode())
                await self.event_loop.run_in_executor( #B
                    None, Kitchen.cook_pizza, order)
                response = f"Your order of {order} pizzas is ready!\n"
            except ValueError:
                response = "Wrong number of pizzas, please try again\n"
 
            print(f"Sending message to {conn.getpeername()}")
            await self.event_loop.sock_sendall(conn, response.encode()) #B
        print(f"Connection with {conn.getpeername()} has been closed")
        conn.close()
 
if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    server = Server(event_loop=event_loop)
    event_loop.create_task(server.start())
    event_loop.run_forever()