import os
import sys
import mandrill
import codecs
import base64


class MailClient(object):

    def send_mail(self, email_to: list, config, subject: str, language='NL', content=None, attachment=None):
        """
        Send a mail with the salureconnect layout and using mandrill
        :param email_to: a list with name and mailadress to who the mail must be send
        :param config: the config file of the project. A mandrill section with at least an api_token, email_from, from_name and email_to with name and mail
        :param subject: The subject of the email
        :param language: Determines the salutation and greeting text. For example Beste or Dear
        :param content: The message of the email
        :param attachment: The attachment of an email loaded as binary file (NOT the location of the file)
        :return: If the sending of the mail is successful or not
        """
        try:
            mandrill_client = mandrill.Mandrill(config.mandrill['api_token'])
            # Load the html template for e-mails
            html_file_location = '{}/templates/mail_salureconnect.html'.format(os.path.dirname(os.path.abspath(__file__)))
            html_file = codecs.open(html_file_location, 'r')
            html = html_file.read()
            opened_attachment = attachment.read()

            if language == 'NL':
                salutation = 'Beste '
                greeting_text = 'Met vriendelijke groet,'
            else:
                salutation = 'Dear '
                greeting_text = 'Kind regards,'

            # Pick the configurations from the config file and create the mail
            for i in email_to:
                new_html = html.replace('{', '{{'). \
                    replace('}', '}}'). \
                    replace('{{subject}}', '{subject}'). \
                    replace('{{title}}', '{title}'). \
                    replace('{{salutation}}', '{salutation}'). \
                    replace('{{name}}', '{name}'). \
                    replace('{{content}}', '{content}'). \
                    replace('{{greeting}}', '{greeting}').format(subject=subject, title=subject, salutation=salutation, name=i['name'], content=content, greeting=greeting_text)
                if attachment == None:
                    mail = {
                        'from_email': config.mandrill['email_from'],
                        'from_name': config.mandrill['name_from'],
                        'subject': subject,
                        'html': new_html,
                        'to': [{'email': i['mail'],
                                'name': i['name'],
                                'type': 'to'}]
                    }
                else:
                    encoded_attachment = base64.b64encode(opened_attachment).decode('utf-8')
                    mail = {
                        'from_email': config.mandrill['email_from'],
                        'from_name': config.mandrill['name_from'],
                        'attachments': [{'content': encoded_attachment,
                                         'name': attachment.name.split('/')[-1]
                                         }],
                        'subject': subject,
                        'html': new_html,
                        'to': [{'email': i['mail'],
                                'name': i['name'],
                                'type': 'to'}]
                    }
                # Send the mail
                mandrill_client.messages.send(message=mail, async=False, ip_pool='Main Pool')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            error = str(e)[:400].replace('\'', '').replace('\"', '') + ' | Line: {}'.format(exc_tb.tb_lineno)
            return Exception(error)
