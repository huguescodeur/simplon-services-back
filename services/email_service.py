import os
from mailjet_rest import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.mailjet = Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3.1'
        )
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.from_name = settings.DEFAULT_FROM_NAME


    def send_welcome_email(self, user, created_by, generated_password):
        """
        Envoie un email de bienvenue avec les informations de connexion
        """
        try:
            html_content = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Bienvenue - Vos informations de connexion</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 20px; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); overflow: hidden; }}
                    .header {{ background: linear-gradient(135deg, #EA6666FF 0%, #E22356FF 100%); color: white; padding: 30px; text-align: center; }}
                    .content {{ padding: 30px; }}
                    .credentials-box {{ background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 8px; padding: 20px; margin: 20px 0; }}
                    .credential-item {{ margin: 10px 0; padding: 10px; background: white; border-radius: 5px; border-left: 4px solid #E22356FF; }}
                    .btn {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Bienvenue sur {settings.COMPANY_NAME} !</h1>
                    </div>
                    
                    <div class="content">
                        <p>Bonjour <strong>{user.first_name} {user.last_name}</strong>,</p>
                        
                        <p>Nous sommes ravis de vous accueillir ! <strong>{created_by.first_name} {created_by.last_name}</strong> ({created_by.get_role_display()}) vous a créé un compte sur notre plateforme.</p>
                        
                        <div class="credentials-box">
                            <h3>📋 Vos informations de connexion :</h3>
                            
                            <div class="credential-item">
                                <strong>👤 Nom d'utilisateur :</strong> {user.username}
                            </div>
                            
                            <div class="credential-item">
                                <strong>📧 Email :</strong> {user.email}
                            </div>
                            
                            <div class="credential-item">
                                <strong>🔑 Mot de passe temporaire :</strong> {generated_password}
                            </div>
                            
                            <div class="credential-item">
                                <strong>🏷️ Rôle :</strong> {user.get_role_display() if hasattr(user, 'get_role_display') else user.role}
                            </div>
                            
                            {f'<div class="credential-item"><strong>🏢 Département :</strong> {user.department}</div>' if user.department else ''}
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Important :</strong> Pour votre sécurité, nous vous recommandons fortement de modifier votre mot de passe lors de votre première connexion. Vous pouvez le faire dans la section "Paramètres" de votre profil.
                        </div>
                        
                        <div style="text-align: center;">
                            <a href="{settings.FRONTEND_URL}/login" class="btn">🚀 Se connecter maintenant</a>
                        </div>
                        
                        <p>Si vous avez des questions ou besoin d'aide, n'hésitez pas à contacter <strong>{created_by.first_name} {created_by.last_name}</strong> ou l'équipe support.</p>
                        
                        <p>À bientôt sur la plateforme !</p>
                        
                        <p>Cordialement,<br>
                        L'équipe {settings.COMPANY_NAME}</p>
                    </div>
                    
                    <div class="footer">
                        <p>Cet email a été envoyé automatiquement. Si vous pensez avoir reçu ce message par erreur, veuillez nous contacter.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            text_content = f"""
Bienvenue sur {settings.COMPANY_NAME} !

Bonjour {user.first_name} {user.last_name},

Nous sommes ravis de vous accueillir ! {created_by.first_name} {created_by.last_name} ({created_by.get_role_display()}) vous a créé un compte sur notre plateforme.

VOS INFORMATIONS DE CONNEXION :
================================
Nom d'utilisateur : {user.username}
Email : {user.email}
Mot de passe temporaire : {generated_password}
Rôle : {user.get_role_display() if hasattr(user, 'get_role_display') else user.role}
{f'Département : {user.department}' if user.department else ''}

IMPORTANT : Pour votre sécurité, nous vous recommandons fortement de modifier votre mot de passe lors de votre première connexion. Vous pouvez le faire dans la section "Paramètres" de votre profil.

Lien de connexion : {settings.FRONTEND_URL}/login

Si vous avez des questions ou besoin d'aide, n'hésitez pas à contacter {created_by.first_name} {created_by.last_name} ou l'équipe support.

À bientôt sur la plateforme !

Cordialement,
L'équipe {settings.COMPANY_NAME}

---
Cet email a été envoyé automatiquement. Si vous pensez avoir reçu ce message par erreur, veuillez nous contacter.
            """

         
            
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": self.from_email,
                            "Name": self.from_name
                        },
                        "To": [
                            {
                                "Email": user.email,
                                "Name": f"{user.first_name} {user.last_name}"
                            }
                        ],
                        "Subject": f"Bienvenue sur {settings.COMPANY_NAME} - Vos informations de connexion",
                        "TextPart": text_content,
                        "HTMLPart": html_content,
                        "CustomID": f"welcome-{user.id}"
                    }
                ]
            }


            result = self.mailjet.send.create(data=data)
            
            if result.status_code == 200:
                logger.info(f"Email de bienvenue envoyé avec succès à {user.email}")
                return True
            else:
                logger.error(f"Erreur lors de l'envoi de l'email: {result.status_code} - {result.json()}")
                return False

        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email de bienvenue: {str(e)}")
            return False

    def send_notification_to_creator(self, creator, new_user):
        """
        Envoie une notification simple à la personne qui a créé l'utilisateur
        """
        try:
            html_content = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
                    .success {{ background: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .user-info {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="success">
                        <h2>✅ Utilisateur créé avec succès</h2>
                    </div>
                    
                    <p>Bonjour <strong>{creator.first_name} {creator.last_name}</strong>,</p>
                    
                    <p>Votre demande de création d'utilisateur a été traitée avec succès !</p>
                    
                    <div class="user-info">
                        <h3>👤 Informations de l'utilisateur créé :</h3>
                        <p><strong>Nom :</strong> {new_user.first_name} {new_user.last_name}</p>
                        <p><strong>Email :</strong> {new_user.email}</p>
                        <p><strong>Nom d'utilisateur :</strong> {new_user.username}</p>
                        <p><strong>Rôle :</strong> {new_user.get_role_display() if hasattr(new_user, 'get_role_display') else new_user.role}</p>
                        {f'<p><strong>Département :</strong> {new_user.department}</p>' if new_user.department else ''}
                    </div>
                    
                    <p>✉️ Un email de bienvenue avec les informations de connexion a été envoyé automatiquement à <strong>{new_user.email}</strong>.</p>
                    
                    <p>Cordialement,<br>L'équipe {settings.COMPANY_NAME}</p>
                </div>
            </body>
            </html>
            """

            text_content = f"""
Utilisateur créé avec succès

Bonjour {creator.first_name} {creator.last_name},

Votre demande de création d'utilisateur a été traitée avec succès !

INFORMATIONS DE L'UTILISATEUR CRÉÉ :
====================================
Nom : {new_user.first_name} {new_user.last_name}
Email : {new_user.email}
Nom d'utilisateur : {new_user.username}
Rôle : {new_user.get_role_display() if hasattr(new_user, 'get_role_display') else new_user.role}
{f'Département : {new_user.department}' if new_user.department else ''}

Un email de bienvenue avec les informations de connexion a été envoyé automatiquement à {new_user.email}.

Cordialement,
L'équipe {settings.COMPANY_NAME}
            """

            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": self.from_email,
                            "Name": self.from_name
                        },
                        "To": [
                            {
                                "Email": creator.email,
                                "Name": f"{creator.first_name} {creator.last_name}"
                            }
                        ],
                        "Subject": f"Utilisateur créé avec succès - {new_user.first_name} {new_user.last_name}",
                        "TextPart": text_content,
                        "HTMLPart": html_content,
                        "CustomID": f"user-created-{new_user.id}"
                    }
                ]
            }

            result = self.mailjet.send.create(data=data)
            
            if result.status_code == 200:
                logger.info(f"Notification envoyée avec succès à {creator.email}")
                return True
            else:
                logger.error(f"Erreur lors de l'envoi de la notification: {result.status_code}")
                return False

        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de la notification: {str(e)}")
            return False
        
    
    def send_purchase_request_notification(self, purchase_request, recipients_role):
        """
        Envoie une notification de nouvelle demande d'achat
        :param purchase_request: L'objet PurchaseRequest
        :param recipients_role: Le rôle des destinataires ('mg' ou 'accounting')
        """
        
        try:
            from core.models import CustomUser  
            from urllib.parse import urljoin

            link = urljoin(settings.FRONTEND_URL, f"requests/{purchase_request.id}")
            
            recipients = CustomUser.objects.filter(role=recipients_role, is_active=True)
            
            if not recipients.exists():
                logger.warning(f"Aucun utilisateur actif trouvé avec le rôle {recipients_role}")
                return False
            
            def format_cost(value):
                return f"{value:,.2f} FCFA" if value is not None else "N/A"
            
            
            if recipients_role == 'mg':
                action_required = "validation"
                next_step = "Moyens Généraux"
                role_display = "Moyens Généraux"
            else:  
                action_required = "étude budgétaire"
                next_step = "Comptabilité"
                role_display = "Comptabilité"
            
            html_content = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Nouvelle demande d'achat</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 20px; }}
                    .container {{ max-width: 700px; margin: 0 auto; background: #ffffff; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); overflow: hidden; }}
                    .header {{ background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; padding: 30px; text-align: center; }}
                    .content {{ padding: 30px; }}
                    .request-box {{ background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 8px; padding: 20px; margin: 20px 0; }}
                    .info-item {{ margin: 15px 0; padding: 12px; background: white; border-radius: 5px; border-left: 4px solid #4CAF50; }}
                    .urgency-high {{ border-left-color: #ff4757; background: #fff5f5; }}
                    .urgency-critical {{ border-left-color: #ff3838; background: #fff0f0; }}
                    .urgency-medium {{ border-left-color: #ffa726; background: #fff8f0; }}
                    .urgency-low {{ border-left-color: #4CAF50; background: #f0fff0; }}
                    .btn {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                    .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 12px; }}
                    .cost {{ font-size: 18px; font-weight: bold; color: #2c3e50; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📋 Nouvelle demande d'achat</h1>
                        <p>Action requise : {action_required}</p>
                    </div>
                    
                    <div class="content">
                        <p>Bonjour,</p>
                        
                        <p>Une nouvelle demande d'achat a été créée et nécessite votre {action_required}.</p>
                        
                        <div class="request-box">
                            <h3>📄 Détails de la demande #{purchase_request.id}</h3>
                            
                            <div class="info-item">
                                <strong>👤 Demandeur :</strong> {purchase_request.user.first_name} {purchase_request.user.last_name} ({purchase_request.user.get_role_display()})
                            </div>
                            
                            <div class="info-item">
                                <strong>📧 Email :</strong> {purchase_request.user.email}
                            </div>
                            
                            {f'<div class="info-item"><strong>🏢 Département :</strong> {purchase_request.user.department}</div>' if purchase_request.user.department else ''}
                            
                            <div class="info-item">
                                <strong>🛍️ Produit/Service :</strong> {purchase_request.item_description}
                            </div>
                            
                            <div class="info-item">
                                <strong>🔢 Quantité :</strong> {purchase_request.quantity}
                            </div>
                            
                            <div class="info-item cost">
                                <strong>💰 Coût estimé :</strong> {format_cost(purchase_request.estimated_cost)}
                            </div>

                            
                            <div class="info-item urgency-{purchase_request.urgency}">
                                <strong>⚡ Urgence :</strong> {purchase_request.get_urgency_display()}
                            </div>
                            
                            <div class="info-item">
                                <strong>📝 Justification :</strong><br>
                                {purchase_request.justification}
                            </div>
                            
                            <div class="info-item">
                                <strong>📅 Date de création :</strong> {purchase_request.created_at.strftime('%d/%m/%Y à %H:%M')}
                            </div>
                            
                            <div class="info-item">
                                <strong>📍 Étape actuelle :</strong> {next_step}
                            </div>
                        </div>
                        
                        <div style="text-align: center;">
                            <a href="{link}" class="btn">🔍 Voir la demande</a>
                        </div>
                        
                        <p><strong>Action requise :</strong> Cette demande attend votre {action_required}. Veuillez vous connecter à la plateforme pour la traiter.</p>
                        
                        <p>Merci pour votre attention.</p>
                        
                        <p>Cordialement,<br>
                        Système de gestion des achats<br>
                        {settings.COMPANY_NAME}</p>
                    </div>
                    
                    <div class="footer">
                        <p>Cet email a été envoyé automatiquement. Veuillez ne pas répondre à ce message.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
    Nouvelle demande d'achat - Action requise

    Bonjour,

    Une nouvelle demande d'achat a été créée et nécessite votre {action_required}.

    DÉTAILS DE LA DEMANDE #{purchase_request.id}
    ==========================================
    Demandeur : {purchase_request.user.first_name} {purchase_request.user.last_name} ({purchase_request.user.get_role_display()})
    Email : {purchase_request.user.email}
    {f'Département : {purchase_request.user.department}' if purchase_request.user.department else ''}

    Produit/Service : {purchase_request.item_description}
    Quantité : {purchase_request.quantity}
    Coût estimé : {format_cost(purchase_request.estimated_cost)}
    Urgence : {purchase_request.get_urgency_display()}

    Justification :
    {purchase_request.justification}

    Date de création : {purchase_request.created_at.strftime('%d/%m/%Y à %H:%M')}
    Étape actuelle : {next_step}

    ACTION REQUISE : Cette demande attend votre {action_required}. Veuillez vous connecter à la plateforme pour la traiter.

    Lien : {settings.FRONTEND_URL}/requests/{purchase_request.id}

    Cordialement,
    Système de gestion des achats
    {settings.COMPANY_NAME}

    ---
    Cet email a été envoyé automatiquement. Veuillez ne pas répondre à ce message.
            """
            
            to_list = []
            for recipient in recipients:
                to_list.append({
                    "Email": recipient.email,
                    "Name": f"{recipient.first_name} {recipient.last_name}"
                })
            
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": self.from_email,
                            "Name": self.from_name
                        },
                        "To": to_list,
                        "Subject": f"🛒 Nouvelle demande d'achat #{purchase_request.id} - {purchase_request.get_urgency_display()} urgence",
                        "TextPart": text_content,
                        "HTMLPart": html_content,
                        "CustomID": f"purchase-request-{purchase_request.id}"
                    }
                ]
            }
            
            
            result = self.mailjet.send.create(data=data)
            
            if result.status_code == 200:
                recipients_emails = [r.email for r in recipients]
                logger.info(f"Notification de demande d'achat #{purchase_request.id} envoyée avec succès à {len(recipients)} {role_display}: {', '.join(recipients_emails)}")
                return True
            else:
                logger.error(f"Erreur lors de l'envoi de la notification de demande: {result.status_code} - {result.json()}")
                return False
        
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de la notification de demande d'achat: {str(e)}")
            return False
        
    
    def send_password_reset_code(self, user, code):
        try:
            html_content = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Code de réinitialisation de mot de passe</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 20px; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); overflow: hidden; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                    .content {{ padding: 30px; }}
                    .code-box {{ background: #f8f9fa; border: 3px solid #667eea; border-radius: 15px; padding: 30px; margin: 25px 0; text-align: center; }}
                    .code {{ font-size: 48px; font-weight: bold; color: #667eea; letter-spacing: 8px; font-family: 'Courier New', monospace; }}
                    .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 12px; }}
                    .security-tips {{ background: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 Réinitialisation de mot de passe</h1>
                    </div>
                    
                    <div class="content">
                        <p>Bonjour <strong>{user.first_name} {user.last_name}</strong>,</p>
                        
                        <p>Vous avez demandé une réinitialisation de votre mot de passe pour votre compte sur {settings.COMPANY_NAME}.</p>
                        
                        <div class="code-box">
                            <p style="margin: 0; font-size: 14px; color: #666;">Votre code de vérification :</p>
                            <div class="code">{code}</div>
                            <p style="margin: 10px 0 0 0; font-size: 12px; color: #888;">
                                ⏰ Ce code expire dans <strong>5 minutes</strong>
                            </p>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Important :</strong> Si vous n'avez pas demandé cette réinitialisation, ignorez cet email. Votre mot de passe actuel reste inchangé.
                        </div>
                        
                        <div class="security-tips">
                            <h4 style="margin-top: 0;">💡 Conseils de sécurité :</h4>
                            <ul style="margin: 10px 0; padding-left: 20px;">
                                <li>Ne partagez jamais ce code avec personne</li>
                                <li>Utilisez un mot de passe unique et complexe</li>
                                <li>Mélangez lettres, chiffres et caractères spéciaux</li>
                                <li>Évitez les informations personnelles dans votre mot de passe</li>
                            </ul>
                        </div>
                        
                        <p>Si vous avez des questions ou des préoccupations, contactez notre équipe support.</p>
                        
                        <p>Cordialement,<br>
                        L'équipe {settings.COMPANY_NAME}</p>
                    </div>
                    
                    <div class="footer">
                        <p>Cet email a été envoyé automatiquement. Ne répondez pas à ce message.</p>
                        <p>Si vous n'arrivez pas à vous connecter, contactez votre administrateur.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            
            text_content = f"""
    Réinitialisation de mot de passe - {settings.COMPANY_NAME}

    Bonjour {user.first_name} {user.last_name},

    Vous avez demandé une réinitialisation de votre mot de passe.

    VOTRE CODE DE VÉRIFICATION : {code}

    IMPORTANT :
    - Ce code expire dans 5 minutes
    - Si vous n'avez pas demandé cette réinitialisation, ignorez cet email
    - Ne partagez jamais ce code avec personne

    CONSEILS DE SÉCURITÉ :
    - Utilisez un mot de passe unique et complexe
    - Mélangez lettres, chiffres et caractères spéciaux
    - Évitez les informations personnelles

    Cordialement,
    L'équipe {settings.COMPANY_NAME}

    ---
    Cet email a été envoyé automatiquement. Ne répondez pas à ce message.
            """

            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": self.from_email,
                            "Name": self.from_name
                        },
                        "To": [
                            {
                                "Email": user.email,
                                "Name": f"{user.first_name} {user.last_name}"
                            }
                        ],
                        "Subject": f"Code de réinitialisation - {settings.COMPANY_NAME}",
                        "TextPart": text_content,
                        "HTMLPart": html_content,
                        "CustomID": f"password-reset-{user.id}-{code}"
                    }
                ]
            }

            
            result = self.mailjet.send.create(data=data)
            
            if result.status_code == 200:
                logger.info(f"Code de réinitialisation envoyé avec succès à {user.email}")
                return True
            else:
                logger.error(f"Erreur lors de l'envoi de l'email: {result.status_code} - {result.json()}")
                return False

        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du code de réinitialisation: {str(e)}")
            return False