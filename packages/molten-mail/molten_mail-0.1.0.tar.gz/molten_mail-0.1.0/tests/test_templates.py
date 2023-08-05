from unittest.mock import MagicMock
from molten import App, Response, Route, testing, HTTP_204
from molten_mail import Mail
from molten_mail.templates import MailTemplates, MailTemplatesComponent


def test_app_can_render_mail_templates():
    mail = Mail(
        user="fake@example.com",
        password="secret",
        port=587,
        use_tls=True,
        suppress_send=True,
    )
    mail.send = MagicMock(return_value=None)

    def template_handler(mail_templates: MailTemplates) -> Response:
        mail.send_message(
            subject="Test email",
            html=mail_templates.render("test_template.html", name="Molten"),
            recipients=["fake@example.com"],
        )
        return Response(HTTP_204, content="")

    app = App(
        components=[MailTemplatesComponent("./tests/mail_templates")],
        routes=[Route("/", template_handler, name="index")],
    )

    client = testing.TestClient(app)

    # Given that a handler will use templating
    # When constructing and email
    response = client.get(app.reverse_uri("index"))

    # Then I should get back a successfull response
    assert response.status_code == 204

    # and the handler should have called the Mail object
    # with the string value of the rendered template
    mail_msg = mail.send.call_args[0][0]
    assert "<th>Hey there Molten</th>" in mail_msg.html
