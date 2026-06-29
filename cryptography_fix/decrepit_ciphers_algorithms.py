#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de remplacement pour cryptography.hazmat.decrepit.ciphers.algorithms
Fournit une implémentation factice de TripleDES pour éviter les erreurs d'importation
"""

class TripleDES:
    """Implémentation factice de TripleDES"""
    
    def __init__(self, key):
        """Initialisation avec la clé"""
        self.key = key
    
    @property
    def key_size(self):
        """Taille de la clé en bits"""
        return len(self.key) * 8
    
    @property
    def block_size(self):
        """Taille du bloc en bits"""
        return 64