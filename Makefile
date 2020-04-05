PROJECT_NAME=2s_lamp_flash

zip:
	$(RM) $(PROJECT_NAME).zip
	zip $(PROJECT_NAME) *[^e].RSS *.pdf
