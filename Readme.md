sequenceDiagram 
    participant Admin as System Admin
    participant VM as Ubuntu VM
    participant TencentDB as Tencent PostgreSQL
    participant TencentRedis as Tencent Redis

    Admin->>VM: 1. Create Ubuntu 22.04 VM
    Admin->>TencentDB: 2. Create PostgreSQL Instance
    Admin->>TencentRedis: 3. Create Redis Instance
    Admin->>VM: 4. SSH into VM
    Admin->>VM: 5. Install Dependencies (Python, Nginx, etc.)
    Admin->>VM: 6. Clone/Upload Application Code
    Admin->>VM: 7. Create Virtual Environment
    Admin->>VM: 8. Configure .env File
    Admin->>VM: 9. Initialize Database
    Admin->>VM: 10. Configure Systemd Service
    Admin->>VM: 11. Configure Nginx
    Admin->>VM: 12. Start & Test Application
