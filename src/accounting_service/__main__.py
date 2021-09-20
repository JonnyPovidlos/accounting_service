if __name__ == '__main__':
    import uvicorn

    from config import Config

    uvicorn.run('accounting_service.app:app',
                host=Config.HOST,
                port=Config.PORT)
