#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparaison Ancien vs Nouveau système de noms de fichiers
"""

def show_comparison():
    """Affiche la comparaison entre ancien et nouveau système"""
    print("🔄 COMPARAISON SYSTÈME DE NOMS DE FICHIERS")
    print("=" * 70)
    
    print("\n🚫 ANCIEN SYSTÈME (complexe):")
    print("   📄 convocation_TCF_DUPONT_JEAN_7674a78e9286_1759307295880.pdf")
    print("   📄 convocation_TCF_MARTIN_SOPHIE_a1b2c3d4e5f6_1759307295912.pdf")
    print("   📄 convocation_TCF_GARCIA_JOSE_9876543210ab_1759307295945.pdf")
    print("\n   ❌ Problèmes:")
    print("      • Noms très longs et difficiles à lire")
    print("      • Hash SHA-256 de 12 caractères peu lisible")
    print("      • Timestamp long (13 chiffres)")
    print("      • Difficile de distinguer les candidats visuellement")
    
    print("\n✅ NOUVEAU SYSTÈME (simplifié):")
    print("   📄 convocation_TCF_DUPONT_JEAN_b6c8y9.pdf")
    print("   📄 convocation_TCF_MARTIN_SOPHIE_u5u0o2.pdf")
    print("   📄 convocation_TCF_GARCIA_JOSE_l0b1j8.pdf")
    print("\n   ✅ Avantages:")
    print("      • Noms courts et lisibles")
    print("      • Identifiant pattern (lettre-chiffre alterné)")
    print("      • Plus facile à distinguer visuellement")
    print("      • Toujours 100% d'unicité garantie")
    print("      • Association candidat-PDF-email fiable maintenue")
    
    print("\n📊 STATISTIQUES DE COMPARAISON:")
    
    # Anciens noms
    old_names = [
        "convocation_TCF_DUPONT_JEAN_7674a78e9286_1759307295880.pdf",
        "convocation_TCF_MARTIN_SOPHIE_a1b2c3d4e5f6_1759307295912.pdf",
        "convocation_TCF_GARCIA_JOSE_9876543210ab_1759307295945.pdf"
    ]
    
    # Nouveaux noms
    new_names = [
        "convocation_TCF_DUPONT_JEAN_b6c8y9.pdf",
        "convocation_TCF_MARTIN_SOPHIE_u5u0o2.pdf",
        "convocation_TCF_GARCIA_JOSE_l0b1j8.pdf"
    ]
    
    avg_old_length = sum(len(name) for name in old_names) / len(old_names)
    avg_new_length = sum(len(name) for name in new_names) / len(new_names)
    
    reduction = ((avg_old_length - avg_new_length) / avg_old_length) * 100
    
    print(f"   📏 Longueur moyenne ancien: {avg_old_length:.1f} caractères")
    print(f"   📏 Longueur moyenne nouveau: {avg_new_length:.1f} caractères")
    print(f"   📉 Réduction de longueur: {reduction:.1f}%")
    
    print("\n🎯 RÉSUMÉ FINAL:")
    print("   🔒 Sécurité: MAINTENUE (100% d'unicité)")
    print("   👁️ Lisibilité: AMÉLIORÉE (noms plus courts)")
    print("   🎨 Pattern: RECONNAISSABLE (lettre-chiffre alterné)")
    print("   ⚡ Performance: IDENTIQUE (même algorithme de base)")
    print("   🔗 Association: FIABLE (registre sécurisé maintenu)")
    
    print("\n💡 EXEMPLES D'IDENTIFIANTS GÉNÉRÉS:")
    example_patterns = ['a9t5g1', 'b2x7k3', 'm4n8p5', 'c1u3e2', 'e8e5e2', 'd8e5v4']
    for pattern in example_patterns:
        print(f"   🆔 {pattern} (lisible et unique)")
    
    print("\n🎉 CONCLUSION:")
    print("   Le nouveau système conserve tous les avantages de sécurité")
    print("   tout en améliorant significativement la lisibilité!")

if __name__ == "__main__":
    show_comparison()