#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface de connexion sécurisée pour l'authentification email
Supporte Outlook, Gmail, et ProtonMail
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from email_auth import EmailAuthenticator

class LoginDialog:
    def __init__(self, parent=None):
        self.parent = parent
        self.result = None
        self.authenticator = EmailAuthenticator()
        self.authenticated = False
        
        # Créer la fenêtre de dialogue
        self.dialog = tk.Toplevel(parent) if parent else tk.Tk()
        self.dialog.title("Connexion Email Sécurisée")
        self.dialog.geometry("450x400")
        self.dialog.resizable(False, False)
        
        # Centrer la fenêtre
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # Frame principal avec padding
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Connexion Email Sécurisée", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(main_frame, 
                              text="Connectez-vous à votre fournisseur d'email pour envoyer les convocations",
                              wraplength=400, justify=tk.CENTER)
        desc_label.pack(pady=(0, 10))
        
        # Note importante pour Outlook
        note_frame = ttk.Frame(main_frame)
        note_frame.pack(fill=tk.X, pady=(0, 20))
        
        note_label = ttk.Label(note_frame, 
                              text="⚠️ Pour Outlook : Utilisez un mot de passe d'application (voir guide)",
                              wraplength=400, justify=tk.CENTER, foreground="orange")
        note_label.pack()
        
        # Bouton d'aide
        help_button = ttk.Button(note_frame, text="📖 Guide de Configuration", 
                                command=self.show_help)
        help_button.pack(pady=(5, 0))
        
        # Frame pour les champs
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Fournisseur d'email
        ttk.Label(fields_frame, text="Fournisseur d'email:").pack(anchor=tk.W, pady=(0, 5))
        self.provider_var = tk.StringVar(value="outlook")
        provider_frame = ttk.Frame(fields_frame)
        provider_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Boutons radio pour les fournisseurs
        providers = [
            ("outlook", "Microsoft Outlook", "🔵"),
            ("gmail", "Gmail", "🔴"),
            ("proton", "ProtonMail", "🟣")
        ]
        
        for value, text, icon in providers:
            rb = ttk.Radiobutton(provider_frame, text=f"{icon} {text}", 
                               variable=self.provider_var, value=value)
            rb.pack(anchor=tk.W, pady=2)
        
        # Adresse email
        ttk.Label(fields_frame, text="Adresse email:").pack(anchor=tk.W, pady=(10, 5))
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(fields_frame, textvariable=self.email_var, width=40)
        self.email_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Mot de passe
        ttk.Label(fields_frame, text="Mot de passe:").pack(anchor=tk.W, pady=(0, 5))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(fields_frame, textvariable=self.password_var, 
                                       show="*", width=40)
        self.password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Case à cocher pour sauvegarder
        self.save_credentials_var = tk.BooleanVar()
        save_cb = ttk.Checkbutton(fields_frame, 
                                 text="Sauvegarder les identifiants de façon sécurisée",
                                 variable=self.save_credentials_var)
        save_cb.pack(anchor=tk.W, pady=(0, 15))
        
        # Frame pour les boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Bouton de test de connexion
        self.test_button = ttk.Button(button_frame, text="Tester la connexion", 
                                     command=self.test_connection)
        self.test_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton de connexion
        self.connect_button = ttk.Button(button_frame, text="Se connecter", 
                                        command=self.connect, style="Accent.TButton")
        self.connect_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton d'annulation
        cancel_button = ttk.Button(button_frame, text="Annuler", command=self.cancel)
        cancel_button.pack(side=tk.RIGHT)
        
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(20, 0))
        self.progress.pack_forget()  # Masquer initialement
        
        # Label de statut
        self.status_label = ttk.Label(main_frame, text="", foreground="blue")
        self.status_label.pack(pady=(10, 0))
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.connect())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # Focus sur le champ email
        self.email_entry.focus()
        
    def show_status(self, message, color="blue"):
        """Affiche un message de statut"""
        self.status_label.config(text=message, foreground=color)
        self.dialog.update()
        
    def show_progress(self, show=True):
        """Affiche ou masque la barre de progression"""
        if show:
            self.progress.pack(fill=tk.X, pady=(20, 0))
            self.progress.start()
        else:
            self.progress.stop()
            self.progress.pack_forget()
        self.dialog.update()
        
    def disable_controls(self, disabled=True):
        """Active ou désactive les contrôles"""
        state = 'disabled' if disabled else 'normal'
        self.email_entry.config(state=state)
        self.password_entry.config(state=state)
        self.test_button.config(state=state)
        self.connect_button.config(state=state)
        
    def test_connection(self):
        """Test la connexion sans sauvegarder"""
        if not self.validate_fields():
            return
            
        def test_thread():
            try:
                self.show_progress(True)
                self.disable_controls(True)
                self.show_status("Test de connexion en cours...", "blue")
                
                # Test d'authentification
                success = self.authenticator.authenticate(
                    self.provider_var.get(),
                    self.email_var.get(),
                    self.password_var.get(),
                    save_credentials=False
                )
                
                if success:
                    self.show_status("✓ Connexion réussie!", "green")
                    messagebox.showinfo("Succès", "Test de connexion réussi!")
                else:
                    self.show_status("✗ Échec de la connexion", "red")
                    
            except Exception as e:
                error_msg = str(e)
                self.show_status(f"✗ Erreur: {error_msg}", "red")
                
                # Message d'erreur spécialisé pour Outlook
                if "Authentication unsuccessful" in error_msg or "535" in error_msg:
                    messagebox.showerror("Erreur d'Authentification Outlook", 
                                       "Authentification échouée.\n\n" +
                                       "Pour Outlook, vous devez utiliser un MOT DE PASSE D'APPLICATION :\n\n" +
                                       "1. Allez sur account.microsoft.com\n" +
                                       "2. Activez l'authentification à 2 facteurs\n" +
                                       "3. Créez un mot de passe d'application\n" +
                                       "4. Utilisez ce mot de passe (16 caractères) au lieu de votre mot de passe habituel\n\n" +
                                       "Consultez le guide de configuration pour plus de détails.")
                else:
                    messagebox.showerror("Erreur", f"Test de connexion échoué:\n{error_msg}")
                
            finally:
                self.show_progress(False)
                self.disable_controls(False)
                
        # Lancer le test dans un thread séparé
        threading.Thread(target=test_thread, daemon=True).start()
        
    def connect(self):
        """Connexion et authentification"""
        if not self.validate_fields():
            return
            
        def connect_thread():
            try:
                self.show_progress(True)
                self.disable_controls(True)
                self.show_status("Connexion en cours...", "blue")
                
                # Authentification
                success = self.authenticator.authenticate(
                    self.provider_var.get(),
                    self.email_var.get(),
                    self.password_var.get(),
                    save_credentials=self.save_credentials_var.get()
                )
                
                if success:
                    self.show_status("✓ Connexion établie!", "green")
                    self.authenticated = True
                    self.result = {
                        'authenticator': self.authenticator,
                        'provider': self.provider_var.get(),
                        'email': self.email_var.get(),
                        'provider_name': self.authenticator.get_provider_info(self.provider_var.get())['name']
                    }
                    
                    # Fermer la fenêtre après un court délai
                    self.dialog.after(1000, self.dialog.destroy)
                else:
                    self.show_status("✗ Échec de la connexion", "red")
                    
            except Exception as e:
                error_msg = str(e)
                self.show_status(f"✗ Erreur: {error_msg}", "red")
                
                # Message d'erreur spécialisé pour Outlook
                if "Authentication unsuccessful" in error_msg or "535" in error_msg:
                    messagebox.showerror("Erreur d'Authentification Outlook", 
                                       "Authentification échouée.\n\n" +
                                       "Pour Outlook, vous devez utiliser un MOT DE PASSE D'APPLICATION :\n\n" +
                                       "1. Allez sur account.microsoft.com\n" +
                                       "2. Activez l'authentification à 2 facteurs\n" +
                                       "3. Créez un mot de passe d'application\n" +
                                       "4. Utilisez ce mot de passe (16 caractères) au lieu de votre mot de passe habituel\n\n" +
                                       "Consultez le guide de configuration pour plus de détails.")
                else:
                    messagebox.showerror("Erreur", f"Connexion échouée:\n{error_msg}")
                    
                self.show_progress(False)
                self.disable_controls(False)
                
        # Lancer la connexion dans un thread séparé
        threading.Thread(target=connect_thread, daemon=True).start()
        
    def validate_fields(self):
        """Valide les champs de saisie"""
        if not self.email_var.get().strip():
            messagebox.showerror("Erreur", "Veuillez saisir votre adresse email")
            self.email_entry.focus()
            return False
            
        if not self.password_var.get():
            messagebox.showerror("Erreur", "Veuillez saisir votre mot de passe")
            self.password_entry.focus()
            return False
            
        if '@' not in self.email_var.get():
            messagebox.showerror("Erreur", "Adresse email invalide")
            self.email_entry.focus()
            return False
            
        return True
        
    def show_help(self):
        """Affiche le guide de configuration"""
        help_text = """
🔐 GUIDE DE CONFIGURATION OUTLOOK

⚠️ PROBLÈME COURANT :
Microsoft Outlook nécessite maintenant un "mot de passe d'application" 
pour les applications tierces comme celle-ci.

📋 SOLUTION (Outlook) :

1. Allez sur https://account.microsoft.com
2. Connectez-vous avec votre compte Outlook
3. Sécurité → Authentification à deux facteurs (activez-la)
4. Sécurité → Options de sécurité avancées
5. Mots de passe d'application → Créer nouveau
6. Nommez-le "Convocation Generator"
7. COPIEZ le mot de passe généré (16 caractères)
8. Utilisez ce mot de passe dans cette application

🔧 DANS CETTE APPLICATION :
- Email : votre adresse Outlook normale
- Mot de passe : le mot de passe d'application (PAS votre mot de passe habituel)

🌐 ALTERNATIVES :
- Gmail : Même principe (mot de passe d'application)
- ProtonMail : Nécessite ProtonMail Bridge

📞 SUPPORT :
Consultez le fichier "outlook_setup_guide.md" pour plus de détails.
        """
        
        help_window = tk.Toplevel(self.dialog)
        help_window.title("Guide de Configuration")
        help_window.geometry("600x500")
        help_window.transient(self.dialog)
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(help_window, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
    def cancel(self):
        """Annule la connexion"""
        self.result = None
        self.dialog.destroy()
        
    def show_modal(self):
        """Affiche la fenêtre de dialogue en mode modal"""
        # Centrer la fenêtre
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Attendre la fermeture de la fenêtre
        self.dialog.wait_window()
        return self.result

def show_login_dialog(parent=None):
    """Fonction utilitaire pour afficher la fenêtre de connexion"""
    dialog = LoginDialog(parent)
    return dialog.show_modal()

if __name__ == "__main__":
    # Test de la fenêtre de connexion
    root = tk.Tk()
    root.withdraw()  # Masquer la fenêtre principale
    
    result = show_login_dialog()
    
    if result:
        print(f"Connexion réussie!")
        print(f"Fournisseur: {result['provider_name']}")
        print(f"Email: {result['email']}")
        
        # Test d'envoi d'email
        try:
            auth = result['authenticator']
            print("Test d'envoi d'email...")
            # auth.send_email("test@example.com", "Test", "<h1>Test</h1>")
            print("✓ Prêt pour l'envoi d'emails")
        except Exception as e:
            print(f"Erreur: {e}")
    else:
        print("Connexion annulée")
    
    root.destroy()