# Путь к переменным окружения
env_path=../__env.env
include $(env_path)
export DEBUG, EXTERNAL_WEB_PORT


run:
	@if [ $(DEBUG) = "true" ]; then \
  		uvicorn main:app --reload --port $(EXTERNAL_WEB_PORT); \
  	elif [ $(DEBUG) = "false" ]; then  \
  	  	uvicorn main:app --port $(EXTERNAL_WEB_PORT); \
  	else \
  	 	echo "Неверный аргумент DEBUG"; \
  	fi;

