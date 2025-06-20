"""
Module d'analyse exploratoire des données (EDA) pour le système de crédit scoring.
Génère des analyses complètes avec commentaires et interprétations automatiques.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class EDAAnalyzer:
    """
    Classe d'analyse exploratoire des données avec commentaires automatiques.
    Suit l'ordre exact du workflow ML défini dans l'architecture.
    """
    
    def __init__(self, data_path: str = "data/processed/credit_cleaned.csv"):
        """Initialisation de l'analyseur EDA"""
        self.data_path = data_path
        self.data = None
        self.report = {}
        self.interpretations = {}
        
        # Configuration des graphiques
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Dossier de sauvegarde
        self.output_dir = "reports/eda"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_cleaned_data(self) -> pd.DataFrame:
        """Chargement des données nettoyées"""
        print("📂 Chargement des données nettoyées...")
        
        try:
            self.data = pd.read_csv(self.data_path)
            print(f"✅ Données chargées : {len(self.data)} lignes, {len(self.data.columns)} colonnes")
            return self.data
        except Exception as e:
            print(f"❌ Erreur de chargement : {e}")
            return None
    
    def comprehensive_analysis(self):
        """
        ÉTAPE 2: Analyse exploratoire complète selon l'architecture
        """
        print("🔍 ÉTAPE 2: ANALYSE EXPLORATOIRE COMPLÈTE")
        print("=" * 60)
        
        if self.data is None:
            self.load_cleaned_data()
            
        if self.data is None:
            print("❌ Impossible de procéder sans données")
            return
        
        # 1. Analyse univariée
        print("\n📊 1. ANALYSE UNIVARIÉE")
        self.univariate_analysis()
        
        # 2. Analyse de la variable cible
        print("\n🎯 2. ANALYSE DE LA VARIABLE CIBLE")
        self.target_analysis()
        
        # 3. Analyse bivariée
        print("\n📈 3. ANALYSE BIVARIÉE")
        self.bivariate_analysis()
        
        # 4. Analyse des corrélations
        print("\n🔗 4. ANALYSE DES CORRÉLATIONS")
        self.correlation_analysis()
        
        # 5. Tests statistiques
        print("\n📏 5. TESTS STATISTIQUES")
        self.statistical_tests()
        
        # 6. Analyses avancées
        print("\n🔬 6. ANALYSES AVANCÉES")
        self.advanced_analysis()
        
        # 7. Génération du rapport final
        print("\n📋 7. GÉNÉRATION DU RAPPORT")
        self.generate_eda_report()
        
        print(f"\n🎉 ANALYSE COMPLÈTE TERMINÉE")
        print(f"📁 Rapports sauvegardés dans : {self.output_dir}")
    
    def univariate_analysis(self):
        """Analyse univariée EXHAUSTIVE avec toutes les visualisations"""
        print("-" * 40)
        
        # Séparation variables numériques et catégorielles
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.data.select_dtypes(include=['object']).columns.tolist()
        
        self.report['univariate'] = {
            'numeric_summary': {},
            'categorical_summary': {},
            'interpretations': {}
        }
        
        # === VARIABLES NUMÉRIQUES - ANALYSE COMPLÈTE ===
        print(f"📊 Variables numériques : {len(numeric_cols)}")
        
        # 1. Distributions de base
        fig, axes = plt.subplots(len(numeric_cols), 3, figsize=(18, 6*len(numeric_cols)))
        fig.suptitle('ANALYSE COMPLÈTE DES VARIABLES NUMÉRIQUES', fontsize=16, fontweight='bold')
        
        for i, col in enumerate(numeric_cols):
            # Statistiques descriptives
            stats = self.data[col].describe()
            self.report['univariate']['numeric_summary'][col] = {
                'count': int(stats['count']),
                'mean': round(stats['mean'], 2),
                'std': round(stats['std'], 2),
                'min': round(stats['min'], 2),
                'max': round(stats['max'], 2),
                'median': round(stats['50%'], 2),
                'q1': round(stats['25%'], 2),
                'q3': round(stats['75%'], 2),
                'skewness': round(self.data[col].skew(), 3),
                'kurtosis': round(self.data[col].kurtosis(), 3)
            }
            
            # Histogramme détaillé
            self.data[col].hist(bins=50, ax=axes[i, 0], alpha=0.7, color='skyblue', edgecolor='black')
            axes[i, 0].set_title(f'Distribution - {col.upper()}', fontweight='bold')
            axes[i, 0].axvline(self.data[col].mean(), color='red', linestyle='--', label=f'Moyenne: {self.data[col].mean():.1f}')
            axes[i, 0].axvline(self.data[col].median(), color='green', linestyle='--', label=f'Médiane: {self.data[col].median():.1f}')
            axes[i, 0].legend()
            
            # Boxplot avec quartiles
            self.data.boxplot(column=col, ax=axes[i, 1])
            axes[i, 1].set_title(f'Boxplot - {col.upper()}', fontweight='bold')
            
            # Densité avec courbe normale
            self.data[col].plot(kind='density', ax=axes[i, 2], color='blue', alpha=0.7)
            axes[i, 2].set_title(f'Densité - {col.upper()}', fontweight='bold')
            
            # Interprétation automatique
            interpretation = self._interpret_numeric_distribution(col, self.data[col])
            self.report['univariate']['interpretations'][col] = interpretation
            print(f"   • {col.upper()}: {interpretation}")
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/distributions_numeriques_completes.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Pairplot des variables numériques
        if len(numeric_cols) > 1:
            import seaborn as sns
            plt.figure(figsize=(12, 10))
            sns.pairplot(self.data[numeric_cols], diag_kind='hist', plot_kws={'alpha': 0.6})
            plt.suptitle('RELATIONS ENTRE VARIABLES NUMÉRIQUES', y=1.02, fontsize=14, fontweight='bold')
            plt.savefig(f"{self.output_dir}/pairplot_variables_numeriques.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        # === VARIABLES CATÉGORIELLES - ANALYSE EXHAUSTIVE ===
        print(f"\n📋 Variables catégorielles : {len(categorical_cols)}")
        
        # Traiter TOUTES les variables catégorielles
        n_cols_per_plot = 3
        n_rows = (len(categorical_cols) + n_cols_per_plot - 1) // n_cols_per_plot
        
        fig, axes = plt.subplots(n_rows, n_cols_per_plot, figsize=(20, 6*n_rows))
        fig.suptitle('DISTRIBUTIONS COMPLÈTES DES VARIABLES CATÉGORIELLES', fontsize=16, fontweight='bold')
        
        if n_rows == 1:
            axes = axes.reshape(1, -1)
        
        for i, col in enumerate(categorical_cols):
            row, col_idx = i // n_cols_per_plot, i % n_cols_per_plot
            
            # Comptage des modalités
            value_counts = self.data[col].value_counts()
            self.report['univariate']['categorical_summary'][col] = {
                'unique_values': int(self.data[col].nunique()),
                'most_frequent': value_counts.index[0],
                'most_frequent_count': int(value_counts.iloc[0]),
                'most_frequent_pct': round((value_counts.iloc[0] / len(self.data)) * 100, 1),
                'entropy': round(-sum([(p/len(self.data))*np.log2(p/len(self.data)) for p in value_counts if p > 0]), 3)
            }
            
            # Graphique en barres - TOUTES les modalités
            if len(value_counts) <= 15:  # Si pas trop de modalités
                value_counts.plot(kind='bar', ax=axes[row, col_idx], color='lightcoral', alpha=0.8)
                axes[row, col_idx].tick_params(axis='x', rotation=45)
            else:  # Si trop de modalités, prendre les top 15
                value_counts.head(15).plot(kind='bar', ax=axes[row, col_idx], color='lightcoral', alpha=0.8)
                axes[row, col_idx].tick_params(axis='x', rotation=45)
                axes[row, col_idx].set_xlabel(f'Top 15 modalités (total: {len(value_counts)})')
            
            axes[row, col_idx].set_title(f'{col.upper()}\n({self.data[col].nunique()} modalités)', fontweight='bold')
            axes[row, col_idx].set_ylabel('Fréquence')
            
            # Interprétation automatique
            interpretation = self._interpret_categorical_distribution(col, value_counts)
            self.report['univariate']['interpretations'][col] = interpretation
            print(f"   • {col.upper()}: {interpretation}")
        
        # Supprimer les axes vides
        for i in range(len(categorical_cols), n_rows * n_cols_per_plot):
            row, col_idx = i // n_cols_per_plot, i % n_cols_per_plot
            fig.delaxes(axes[row, col_idx])
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/distributions_categoriques_completes.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Analyse univariée EXHAUSTIVE terminée")
    
    def target_analysis(self):
        """Analyse approfondie de la variable cible"""
        print("-" * 40)
        
        target_col = 'cible'
        if target_col not in self.data.columns:
            print("❌ Variable cible 'cible' non trouvée")
            return
        
        # Distribution de la cible
        target_dist = self.data[target_col].value_counts()
        target_pct = self.data[target_col].value_counts(normalize=True) * 100
        
        self.report['target_analysis'] = {
            'distribution': target_dist.to_dict(),
            'percentages': target_pct.round(1).to_dict(),
            'total_count': len(self.data)
        }
        
        # Visualisation
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('ANALYSE DE LA VARIABLE CIBLE', fontsize=16, fontweight='bold')
        
        # Graphique en barres
        target_dist.plot(kind='bar', ax=ax1, color=['lightgreen', 'salmon'], alpha=0.8)
        ax1.set_title('Distribution de la Variable Cible', fontweight='bold')
        ax1.set_xlabel('Statut de Remboursement')
        ax1.set_ylabel('Nombre de Clients')
        ax1.tick_params(axis='x', rotation=45)
        
        # Graphique en secteurs
        target_pct.plot(kind='pie', ax=ax2, autopct='%1.1f%%', startangle=90, 
                       colors=['lightgreen', 'salmon'])
        ax2.set_title('Répartition en Pourcentage', fontweight='bold')
        ax2.set_ylabel('')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/analyse_variable_cible.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # Interprétation de la cible
        interpretation = self._interpret_target_distribution(target_dist, target_pct)
        self.report['target_analysis']['interpretation'] = interpretation
        print(f"🎯 {interpretation}")
        
        print("✅ Analyse de la variable cible terminée")
    
    def bivariate_analysis(self):
        """Analyse bivariée EXHAUSTIVE : relations entre variables et cible"""
        print("-" * 40)
        
        target_col = 'cible'
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.data.select_dtypes(include=['object']).columns.tolist()
        categorical_cols = [col for col in categorical_cols if col != target_col]  # Exclure la cible
        
        self.report['bivariate'] = {
            'numeric_vs_target': {},
            'categorical_vs_target': {},
            'interpretations': {}
        }
        
        # === TOUTES LES VARIABLES NUMÉRIQUES vs CIBLE ===
        print("📊 Relations TOUTES Variables Numériques vs Cible")
        
        n_numeric = len(numeric_cols)
        if n_numeric > 0:
            # Graphiques multiples pour variables numériques
            fig, axes = plt.subplots(n_numeric, 3, figsize=(18, 6*n_numeric))
            fig.suptitle('ANALYSE EXHAUSTIVE: Variables Numériques vs Cible', fontsize=16, fontweight='bold')
            
            if n_numeric == 1:
                axes = axes.reshape(1, -1)
            
            for i, col in enumerate(numeric_cols):
                # Boxplot par catégorie de cible
                self.data.boxplot(column=col, by=target_col, ax=axes[i, 0])
                axes[i, 0].set_title(f'Boxplot: {col.upper()}')
                
                # Histogrammes superposés
                for target_val in self.data[target_col].unique():
                    subset = self.data[self.data[target_col] == target_val][col]
                    axes[i, 1].hist(subset, alpha=0.6, label=target_val, bins=30)
                axes[i, 1].set_title(f'Distributions: {col.upper()}')
                axes[i, 1].legend()
                
                # Violin plot
                import seaborn as sns
                sns.violinplot(data=self.data, x=target_col, y=col, ax=axes[i, 2])
                axes[i, 2].set_title(f'Densités: {col.upper()}')
                axes[i, 2].tick_params(axis='x', rotation=45)
                
                # Statistiques par groupe
                stats_by_target = self.data.groupby(target_col)[col].agg(['mean', 'median', 'std', 'min', 'max']).round(2)
                self.report['bivariate']['numeric_vs_target'][col] = stats_by_target.to_dict()
                
                # Interprétation
                interpretation = self._interpret_numeric_vs_target(col, stats_by_target)
                self.report['bivariate']['interpretations'][f"{col}_vs_target"] = interpretation
                print(f"   • {col.upper()}: {interpretation}")
            
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/toutes_variables_numeriques_vs_cible.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        # === TOUTES LES VARIABLES CATÉGORIELLES vs CIBLE ===
        print(f"\n📋 Relations TOUTES Variables Catégorielles vs Cible")
        
        # Traiter par groupes de 4 variables
        n_per_plot = 4
        n_plots = (len(categorical_cols) + n_per_plot - 1) // n_per_plot
        
        for plot_idx in range(n_plots):
            start_idx = plot_idx * n_per_plot
            end_idx = min(start_idx + n_per_plot, len(categorical_cols))
            current_cols = categorical_cols[start_idx:end_idx]
            
            fig, axes = plt.subplots(2, len(current_cols), figsize=(5*len(current_cols), 12))
            fig.suptitle(f'Variables Catégorielles vs Cible (Groupe {plot_idx+1})', fontsize=16, fontweight='bold')
            
            if len(current_cols) == 1:
                axes = axes.reshape(-1, 1)
            
            for i, col in enumerate(current_cols):
                # Tableau croisé en pourcentages
                crosstab = pd.crosstab(self.data[col], self.data[target_col], normalize='index') * 100
                self.report['bivariate']['categorical_vs_target'][col] = crosstab.round(1).to_dict()
                
                # Graphique empilé (pourcentages)
                crosstab.plot(kind='bar', stacked=True, ax=axes[0, i], 
                             color=['lightgreen', 'salmon'], alpha=0.8)
                axes[0, i].set_title(f'{col.upper()}\n(% par modalité)')
                axes[0, i].set_ylabel('Pourcentage')
                axes[0, i].legend(title='Statut', bbox_to_anchor=(1.05, 1), loc='upper left')
                axes[0, i].tick_params(axis='x', rotation=45)
                
                # Graphique en effectifs absolus
                crosstab_abs = pd.crosstab(self.data[col], self.data[target_col])
                crosstab_abs.plot(kind='bar', ax=axes[1, i], 
                                 color=['lightgreen', 'salmon'], alpha=0.8)
                axes[1, i].set_title(f'{col.upper()}\n(Effectifs absolus)')
                axes[1, i].set_ylabel('Nombre de clients')
                axes[1, i].legend(title='Statut', bbox_to_anchor=(1.05, 1), loc='upper left')
                axes[1, i].tick_params(axis='x', rotation=45)
                
                # Interprétation
                interpretation = self._interpret_categorical_vs_target(col, crosstab)
                self.report['bivariate']['interpretations'][f"{col}_vs_target"] = interpretation
                print(f"   • {col.upper()}: {interpretation}")
            
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/variables_categoriques_vs_cible_groupe{plot_idx+1}.png", 
                       dpi=300, bbox_inches='tight')
            plt.close()
        
        # === HEATMAP DES ASSOCIATIONS ===
        print(f"\n🔥 Création de la heatmap des associations")
        self._create_association_heatmap(categorical_cols, target_col)
        
        print("✅ Analyse bivariée EXHAUSTIVE terminée")
        
    def _create_association_heatmap(self, categorical_cols, target_col):
        """Créer une heatmap des forces d'association avec la cible"""
        from scipy.stats import chi2_contingency
        
        associations = []
        col_names = []
        
        # Calculer les associations pour variables catégorielles
        for col in categorical_cols:
            try:
                contingency_table = pd.crosstab(self.data[col], self.data[target_col])
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                # Cramér's V comme mesure d'association
                n = contingency_table.sum().sum()
                cramers_v = np.sqrt(chi2 / (n * (min(contingency_table.shape) - 1)))
                associations.append(cramers_v)
                col_names.append(col)
            except:
                associations.append(0)
                col_names.append(col)
        
        # Ajouter les corrélations pour variables numériques
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Encoder la variable cible pour corrélation
        target_encoded = pd.get_dummies(self.data[target_col]).iloc[:, 0]
        
        for col in numeric_cols:
            corr = abs(self.data[col].corr(target_encoded))
            associations.append(corr)
            col_names.append(col)
        
        # Créer la heatmap
        plt.figure(figsize=(3, len(col_names)*0.5))
        association_df = pd.DataFrame({
            'Variable': col_names,
            'Association avec Cible': associations
        }).set_index('Variable').sort_values('Association avec Cible', ascending=True)
        
        import seaborn as sns
        sns.heatmap(association_df, annot=True, cmap='YlOrRd', cbar_kws={'label': 'Force d\'association'})
        plt.title('FORCE D\'ASSOCIATION AVEC LA VARIABLE CIBLE', fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/heatmap_associations_cible.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def correlation_analysis(self):
        """Analyse EXHAUSTIVE des corrélations entre toutes les variables"""
        print("-" * 40)
        
        # Variables numériques seulement
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if numeric_data.empty:
            print("❌ Aucune variable numérique pour l'analyse de corrélation")
            return
        
        # Matrice de corrélation
        correlation_matrix = numeric_data.corr()
        self.report['correlation'] = {
            'matrix': correlation_matrix.round(3).to_dict(),
            'high_correlations': {},
            'all_correlations': {},
            'interpretations': {}
        }
        
        # === ANALYSE DÉTAILLÉE DES CORRÉLATIONS ===
        print("🔗 Analyse complète des corrélations")
        
        # Toutes les corrélations par seuil
        all_corr_pairs = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                all_corr_pairs.append({
                    'var1': correlation_matrix.columns[i],
                    'var2': correlation_matrix.columns[j],
                    'correlation': round(corr_value, 3),
                    'abs_correlation': round(abs(corr_value), 3)
                })
        
        # Trier par corrélation absolue décroissante
        all_corr_pairs = sorted(all_corr_pairs, key=lambda x: x['abs_correlation'], reverse=True)
        self.report['correlation']['all_correlations'] = all_corr_pairs
        
        # Catégoriser les corrélations
        strong_corr = [p for p in all_corr_pairs if p['abs_correlation'] > 0.7]
        moderate_corr = [p for p in all_corr_pairs if 0.3 < p['abs_correlation'] <= 0.7]
        weak_corr = [p for p in all_corr_pairs if 0.1 < p['abs_correlation'] <= 0.3]
        
        self.report['correlation']['high_correlations'] = strong_corr
        
        print(f"   • Corrélations fortes (>0.7): {len(strong_corr)}")
        print(f"   • Corrélations modérées (0.3-0.7): {len(moderate_corr)}")
        print(f"   • Corrélations faibles (0.1-0.3): {len(weak_corr)}")
        
        # === VISUALISATIONS MULTIPLES ===
        
        # 1. Matrice de corrélation classique
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdYlBu_r', 
                   center=0, square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        plt.title('MATRICE DE CORRÉLATION - Variables Numériques', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/matrice_correlation_complete.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Heatmap des corrélations absolues
        plt.figure(figsize=(12, 10))
        correlation_abs = correlation_matrix.abs()
        sns.heatmap(correlation_abs, mask=mask, annot=True, cmap='Reds', 
                   square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        plt.title('MATRICE DES CORRÉLATIONS ABSOLUES', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/matrice_correlation_absolue.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Graphique en barres des corrélations les plus fortes
        if len(all_corr_pairs) > 0:
            top_corr = all_corr_pairs[:min(10, len(all_corr_pairs))]  # Top 10
            
            plt.figure(figsize=(12, 8))
            labels = [f"{p['var1']} vs {p['var2']}" for p in top_corr]
            values = [p['correlation'] for p in top_corr]
            colors = ['red' if v < 0 else 'blue' for v in values]
            
            plt.barh(range(len(labels)), values, color=colors, alpha=0.7)
            plt.yticks(range(len(labels)), labels)
            plt.xlabel('Corrélation')
            plt.title('TOP 10 DES CORRÉLATIONS LES PLUS FORTES', fontweight='bold')
            plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
            plt.axvline(x=0.5, color='orange', linestyle='--', alpha=0.5, label='Seuil modéré (0.5)')
            plt.axvline(x=-0.5, color='orange', linestyle='--', alpha=0.5)
            plt.axvline(x=0.7, color='red', linestyle='--', alpha=0.5, label='Seuil fort (0.7)')
            plt.axvline(x=-0.7, color='red', linestyle='--', alpha=0.5)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/top_correlations.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        # 4. Scatter plots des corrélations les plus importantes
        if len(strong_corr + moderate_corr) > 0:
            important_corr = (strong_corr + moderate_corr)[:6]  # Top 6 corrélations importantes
            
            n_plots = len(important_corr)
            n_cols = 3
            n_rows = (n_plots + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
            fig.suptitle('SCATTER PLOTS DES CORRÉLATIONS IMPORTANTES', fontsize=16, fontweight='bold')
            
            if n_rows == 1:
                axes = axes.reshape(1, -1) if n_plots > 1 else [axes]
            
            for i, corr_pair in enumerate(important_corr):
                row, col = i // n_cols, i % n_cols
                ax = axes[row, col] if n_rows > 1 else axes[col]
                
                var1, var2 = corr_pair['var1'], corr_pair['var2']
                corr_val = corr_pair['correlation']
                
                axes[i].scatter(self.data[var1], self.data[var2], alpha=0.6, color='blue')
                axes[i].set_xlabel(var1)
                axes[i].set_ylabel(var2)
                axes[i].set_title(f'{var1} vs {var2}\n(r = {corr_val})')
                
                # Ligne de tendance
                z = np.polyfit(self.data[var1], self.data[var2], 1)
                p = np.poly1d(z)
                axes[i].plot(self.data[var1], p(self.data[var1]), "r--", alpha=0.8)
            
            # Supprimer les axes vides
            for i in range(n_plots, n_rows * n_cols):
                row, col = i // n_cols, i % n_cols
                ax = axes[row, col] if n_rows > 1 else axes[col]
                fig.delaxes(ax)
            
            plt.tight_layout()
            plt.savefig(f"{self.output_dir}/scatter_plots_correlations.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        # === INTERPRÉTATIONS DÉTAILLÉES ===
        print("\n📊 Résultats détaillés :")
        
        if strong_corr:
            print("   🔴 Corrélations FORTES (>0.7) :")
            for pair in strong_corr:
                interpretation = f"Corrélation FORTE {pair['correlation']} entre {pair['var1']} et {pair['var2']}"
                print(f"      • {interpretation}")
                self.report['correlation']['interpretations'][f"{pair['var1']}_vs_{pair['var2']}"] = interpretation
        
        if moderate_corr:
            print("   🟡 Corrélations MODÉRÉES (0.3-0.7) :")
            for pair in moderate_corr[:5]:  # Top 5 seulement
                interpretation = f"Corrélation modérée {pair['correlation']} entre {pair['var1']} et {pair['var2']}"
                print(f"      • {interpretation}")
                self.report['correlation']['interpretations'][f"{pair['var1']}_vs_{pair['var2']}"] = interpretation
        
        if not strong_corr and not moderate_corr:
            print("   ✅ Pas de corrélation significative détectée")
            self.report['correlation']['interpretations']['general'] = "Variables numériques peu corrélées entre elles"
        
        print("✅ Analyse des corrélations EXHAUSTIVE terminée")
    
    def statistical_tests(self):
        """Tests statistiques de significativité"""
        print("-" * 40)
        
        from scipy.stats import chi2_contingency, ttest_ind
        
        target_col = 'cible'
        self.report['statistical_tests'] = {
            'chi2_tests': {},
            'ttest_results': {},
            'interpretations': {}
        }
        
        # === TESTS CHI-2 pour variables catégorielles ===
        print("📏 Tests Chi-2 (variables catégorielles vs cible)")
        categorical_cols = ['historique', 'objet', 'statut', 'emploi']
        
        for col in categorical_cols[:3]:  # Top 3
            if col in self.data.columns:
                try:
                    contingency_table = pd.crosstab(self.data[col], self.data[target_col])
                    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                    
                    self.report['statistical_tests']['chi2_tests'][col] = {
                        'chi2': round(chi2, 3),
                        'p_value': round(p_value, 6),
                        'significant': p_value < 0.05
                    }
                    
                    # Interprétation
                    if p_value < 0.05:
                        interpretation = f"Association SIGNIFICATIVE avec la cible (p={p_value:.4f})"
                    else:
                        interpretation = f"Association NON significative avec la cible (p={p_value:.4f})"
                    
                    self.report['statistical_tests']['interpretations'][f"chi2_{col}"] = interpretation
                    print(f"   • {col.upper()}: {interpretation}")
                    
                except Exception as e:
                    print(f"   • {col.upper()}: Erreur dans le test Chi-2")
        
        # === TESTS T pour variables numériques ===
        print(f"\n📊 Tests T de Student (variables numériques vs cible)")
        numeric_cols = ['duree', 'montant', 'age']
        
        for col in numeric_cols:
            if col in self.data.columns:
                try:
                    # Séparation par groupes de cible
                    group1 = self.data[self.data[target_col] == self.data[target_col].unique()[0]][col]
                    group2 = self.data[self.data[target_col] == self.data[target_col].unique()[1]][col]
                    
                    # Test t
                    t_stat, p_value = ttest_ind(group1, group2)
                    
                    self.report['statistical_tests']['ttest_results'][col] = {
                        't_statistic': round(t_stat, 3),
                        'p_value': round(p_value, 6),
                        'significant': p_value < 0.05
                    }
                    
                    # Interprétation
                    if p_value < 0.05:
                        interpretation = f"Différence SIGNIFICATIVE entre groupes (p={p_value:.4f})"
                    else:
                        interpretation = f"Différence NON significative entre groupes (p={p_value:.4f})"
                    
                    self.report['statistical_tests']['interpretations'][f"ttest_{col}"] = interpretation
                    print(f"   • {col.upper()}: {interpretation}")
                    
                except Exception as e:
                    print(f"   • {col.upper()}: Erreur dans le test T")
        
        print("✅ Tests statistiques terminés")
    
    def advanced_analysis(self):
        """Analyses avancées pour une EDA professionnelle"""
        print("-" * 40)
        
        self.report['advanced_analysis'] = {
            'outliers_analysis': {},
            'clustering_analysis': {},
            'risk_segmentation': {},
            'mutual_information': {},
            'variable_interactions': {},
            'missing_patterns': {},
            'stability_analysis': {},
            'interpretations': {}
        }
        
        # 1. Analyse détaillée des outliers
        self._advanced_outliers_analysis()
        
        # 2. Clustering automatique des clients
        self._clustering_analysis()
        
        # 3. Segmentation par niveau de risque
        self._risk_segmentation()
        
        # 4. Information mutuelle entre variables
        self._mutual_information_analysis()
        
        # 5. Analyse des interactions entre variables
        self._variable_interactions_analysis()
        
        # 6. Patterns des données manquantes
        self._missing_patterns_analysis()
        
        # 7. Analyse de stabilité (PSI)
        self._stability_analysis()
        
        print("✅ Analyses avancées terminées")
    
    def _advanced_outliers_analysis(self):
        """Analyse détaillée des outliers avec plusieurs méthodes"""
        print("\n🔍 Analyse avancée des outliers")
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        outliers_summary = {}
        
        for col in numeric_cols:
            data_col = self.data[col].dropna()
            
            # Méthode 1: IQR
            Q1 = data_col.quantile(0.25)
            Q3 = data_col.quantile(0.75)
            IQR = Q3 - Q1
            iqr_outliers = data_col[(data_col < Q1 - 1.5*IQR) | (data_col > Q3 + 1.5*IQR)]
            
            # Méthode 2: Z-score
            z_scores = np.abs((data_col - data_col.mean()) / data_col.std())
            zscore_outliers = data_col[z_scores > 3]
            
            # Méthode 3: Percentiles extrêmes
            p1, p99 = data_col.quantile([0.01, 0.99])
            percentile_outliers = data_col[(data_col < p1) | (data_col > p99)]
            
            outliers_summary[col] = {
                'iqr_outliers': len(iqr_outliers),
                'zscore_outliers': len(zscore_outliers),
                'percentile_outliers': len(percentile_outliers),
                'iqr_percentage': round(len(iqr_outliers)/len(data_col)*100, 2),
                'zscore_percentage': round(len(zscore_outliers)/len(data_col)*100, 2),
                'percentile_percentage': round(len(percentile_outliers)/len(data_col)*100, 2)
            }
            
            print(f"   • {col.upper()}:")
            print(f"     - IQR: {len(iqr_outliers)} outliers ({outliers_summary[col]['iqr_percentage']}%)")
            print(f"     - Z-score: {len(zscore_outliers)} outliers ({outliers_summary[col]['zscore_percentage']}%)")
            print(f"     - Percentiles: {len(percentile_outliers)} outliers ({outliers_summary[col]['percentile_percentage']}%)")
        
        self.report['advanced_analysis']['outliers_analysis'] = outliers_summary
        
        # Visualisation comparative des méthodes d'outliers
        fig, axes = plt.subplots(len(numeric_cols), 1, figsize=(12, 4*len(numeric_cols)))
        fig.suptitle('COMPARAISON DES MÉTHODES DE DÉTECTION D\'OUTLIERS', fontsize=16, fontweight='bold')
        
        if len(numeric_cols) == 1:
            axes = [axes]
        
        for i, col in enumerate(numeric_cols):
            methods = ['IQR', 'Z-score', 'Percentiles']
            counts = [outliers_summary[col]['iqr_outliers'], 
                     outliers_summary[col]['zscore_outliers'],
                     outliers_summary[col]['percentile_outliers']]
            
            axes[i].bar(methods, counts, color=['skyblue', 'lightgreen', 'salmon'], alpha=0.8)
            axes[i].set_title(f'Outliers détectés - {col.upper()}', fontweight='bold')
            axes[i].set_ylabel('Nombre d\'outliers')
            
            # Ajouter les pourcentages sur les barres
            for j, count in enumerate(counts):
                percentage = [outliers_summary[col]['iqr_percentage'], 
                            outliers_summary[col]['zscore_percentage'],
                            outliers_summary[col]['percentile_percentage']][j]
                axes[i].text(j, count + max(counts)*0.01, f'{percentage}%', 
                           ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/analyse_outliers_avancee.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _clustering_analysis(self):
        """Clustering automatique des clients"""
        print("\n🎯 Clustering automatique des clients")
        
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        
        # Préparer les données pour le clustering
        clustering_data = self.data.copy()
        
        # Encoder les variables catégorielles
        label_encoders = {}
        for col in clustering_data.select_dtypes(include=['object']).columns:
            if col != 'cible':
                le = LabelEncoder()
                clustering_data[col] = le.fit_transform(clustering_data[col].astype(str))
                label_encoders[col] = le
        
        # Exclure la variable cible
        features = clustering_data.drop('cible', axis=1)
        
        # Standardisation
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # Déterminer le nombre optimal de clusters (méthode du coude)
        inertias = []
        k_range = range(2, 8)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(features_scaled)
            inertias.append(kmeans.inertia_)
        
        # Clustering avec k optimal (on prend 4 clusters)
        optimal_k = 4
        kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(features_scaled)
        
        # Analyser les clusters
        clustering_data['cluster'] = cluster_labels
        
        cluster_analysis = {}
        for cluster in range(optimal_k):
            cluster_data = clustering_data[clustering_data['cluster'] == cluster]
            cluster_analysis[f'cluster_{cluster}'] = {
                'size': len(cluster_data),
                'percentage': round(len(cluster_data)/len(clustering_data)*100, 1),
                'default_rate': round(len(cluster_data[cluster_data['cible'] == 'credit avec impaye'])/len(cluster_data)*100, 1)
            }
            
            print(f"   • Cluster {cluster}: {len(cluster_data)} clients ({cluster_analysis[f'cluster_{cluster}']['percentage']}%)")
            print(f"     - Taux de défaut: {cluster_analysis[f'cluster_{cluster}']['default_rate']}%")
        
        self.report['advanced_analysis']['clustering_analysis'] = cluster_analysis
        
        # Visualisation des clusters
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('ANALYSE DES CLUSTERS DE CLIENTS', fontsize=16, fontweight='bold')
        
        # Graphique 1: Tailles des clusters
        cluster_sizes = [cluster_analysis[f'cluster_{i}']['size'] for i in range(optimal_k)]
        axes[0].pie(cluster_sizes, labels=[f'Cluster {i}' for i in range(optimal_k)], autopct='%1.1f%%')
        axes[0].set_title('Répartition des clients par cluster')
        
        # Graphique 2: Taux de défaut par cluster
        default_rates = [cluster_analysis[f'cluster_{i}']['default_rate'] for i in range(optimal_k)]
        bars = axes[1].bar(range(optimal_k), default_rates, color=['green' if x < 30 else 'orange' if x < 50 else 'red' for x in default_rates])
        axes[1].set_title('Taux de défaut par cluster')
        axes[1].set_xlabel('Cluster')
        axes[1].set_ylabel('Taux de défaut (%)')
        axes[1].set_xticks(range(optimal_k))
        
        # Ajouter les valeurs sur les barres
        for i, bar in enumerate(bars):
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{default_rates[i]:.1f}%', ha='center', va='bottom')
        
        # Graphique 3: Méthode du coude
        axes[2].plot(k_range, inertias, 'bo-')
        axes[2].set_title('Méthode du coude pour K optimal')
        axes[2].set_xlabel('Nombre de clusters')
        axes[2].set_ylabel('Inertie')
        axes[2].axvline(x=optimal_k, color='red', linestyle='--', alpha=0.7, label=f'K choisi = {optimal_k}')
        axes[2].legend()
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/analyse_clustering.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _risk_segmentation(self):
        """Segmentation par niveau de risque"""
        print("\n📊 Segmentation par niveau de risque")
        
        # Variables numériques pour créer un score de risque simple
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Score de risque basé sur les variables numériques (exemple simple)
        risk_score = 0
        for col in numeric_cols:
            # Normaliser et pondérer (exemple basique)
            normalized = (self.data[col] - self.data[col].min()) / (self.data[col].max() - self.data[col].min())
            if col == 'duree':  # Plus de durée = plus de risque
                risk_score += normalized * 0.4
            elif col == 'montant':  # Plus de montant = plus de risque
                risk_score += normalized * 0.4
            elif col == 'age':  # Relation complexe avec l'âge
                risk_score += (1 - normalized) * 0.2  # Inversé pour l'âge
        
        # Créer des déciles de risque
        self.data['risk_score'] = risk_score
        self.data['risk_decile'] = pd.qcut(risk_score, 10, labels=[f'D{i}' for i in range(1, 11)])
        
        # Analyser chaque décile
        decile_analysis = {}
        for decile in [f'D{i}' for i in range(1, 11)]:
            decile_data = self.data[self.data['risk_decile'] == decile]
            if len(decile_data) > 0:
                decile_analysis[decile] = {
                    'size': len(decile_data),
                    'default_rate': round(len(decile_data[decile_data['cible'] == 'credit avec impaye'])/len(decile_data)*100, 1),
                    'avg_amount': round(decile_data['montant'].mean(), 0),
                    'avg_duration': round(decile_data['duree'].mean(), 1)
                }
        
        self.report['advanced_analysis']['risk_segmentation'] = decile_analysis
        
        # Affichage des résultats
        print("   Analyse par décile de risque:")
        for decile, stats in decile_analysis.items():
            print(f"   • {decile}: {stats['default_rate']}% de défaut, "
                  f"{stats['avg_amount']:.0f}€ moyen, {stats['avg_duration']:.1f} mois")
        
        # Visualisation de la segmentation
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('SEGMENTATION PAR NIVEAU DE RISQUE', fontsize=16, fontweight='bold')
        
        deciles = list(decile_analysis.keys())
        default_rates = [decile_analysis[d]['default_rate'] for d in deciles]
        sizes = [decile_analysis[d]['size'] for d in deciles]
        avg_amounts = [decile_analysis[d]['avg_amount'] for d in deciles]
        avg_durations = [decile_analysis[d]['avg_duration'] for d in deciles]
        
        # Graphique 1: Taux de défaut par décile
        axes[0,0].bar(deciles, default_rates, color='red', alpha=0.7)
        axes[0,0].set_title('Taux de défaut par décile de risque')
        axes[0,0].set_ylabel('Taux de défaut (%)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Graphique 2: Taille des déciles
        axes[0,1].bar(deciles, sizes, color='blue', alpha=0.7)
        axes[0,1].set_title('Nombre de clients par décile')
        axes[0,1].set_ylabel('Nombre de clients')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Graphique 3: Montant moyen par décile
        axes[1,0].bar(deciles, avg_amounts, color='green', alpha=0.7)
        axes[1,0].set_title('Montant moyen par décile')
        axes[1,0].set_ylabel('Montant moyen (€)')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Graphique 4: Durée moyenne par décile
        axes[1,1].bar(deciles, avg_durations, color='orange', alpha=0.7)
        axes[1,1].set_title('Durée moyenne par décile')
        axes[1,1].set_ylabel('Durée moyenne (mois)')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/segmentation_risque.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _mutual_information_analysis(self):
        """Analyse de l'information mutuelle entre variables"""
        print("\n🧠 Information mutuelle entre variables")
        
        from sklearn.feature_selection import mutual_info_classif
        from sklearn.preprocessing import LabelEncoder
        
        # Préparer les données
        features_data = self.data.copy()
        
        # Encoder toutes les variables catégorielles
        for col in features_data.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            features_data[col] = le.fit_transform(features_data[col].astype(str))
        
        # Séparer features et target
        X = features_data.drop('cible', axis=1)
        y = features_data['cible']
        
        # Calculer l'information mutuelle
        mi_scores = mutual_info_classif(X, y, random_state=42)
        
        # Créer un DataFrame des scores
        mi_df = pd.DataFrame({
            'Variable': X.columns,
            'Mutual_Information': mi_scores
        }).sort_values('Mutual_Information', ascending=False)
        
        self.report['advanced_analysis']['mutual_information'] = mi_df.to_dict('records')
        
        print("   Variables classées par information mutuelle:")
        for _, row in mi_df.head(10).iterrows():
            print(f"   • {row['Variable']}: {row['Mutual_Information']:.4f}")
        
        # Visualisation
        plt.figure(figsize=(12, 8))
        top_15 = mi_df.head(15)
        plt.barh(range(len(top_15)), top_15['Mutual_Information'], color='purple', alpha=0.7)
        plt.yticks(range(len(top_15)), top_15['Variable'])
        plt.xlabel('Information Mutuelle')
        plt.title('INFORMATION MUTUELLE AVEC LA VARIABLE CIBLE', fontweight='bold')
        plt.gca().invert_yaxis()
        
        # Ajouter une ligne de référence
        plt.axvline(x=mi_df['Mutual_Information'].mean(), color='red', linestyle='--', 
                   alpha=0.7, label=f'Moyenne: {mi_df["Mutual_Information"].mean():.4f}')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/information_mutuelle.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _variable_interactions_analysis(self):
        """Analyse des interactions entre variables importantes"""
        print("\n🔄 Interactions entre variables importantes")
        
        # Prendre les variables les plus importantes (top 5)
        important_vars = ['duree', 'montant', 'historique', 'objet', 'statut']
        
        interactions_summary = {}
        
        # Analyser les interactions 2 à 2
        for i, var1 in enumerate(important_vars):
            for var2 in important_vars[i+1:]:
                # Créer des groupes combinés
                if self.data[var1].dtype == 'object' and self.data[var2].dtype == 'object':
                    # Deux variables catégorielles
                    combined = self.data[var1].astype(str) + ' + ' + self.data[var2].astype(str)
                    crosstab = pd.crosstab(combined, self.data['cible'], normalize='index') * 100
                    
                    # Calculer la variance des taux de défaut
                    default_rates = crosstab.iloc[:, 1] if 'credit avec impaye' in crosstab.columns else crosstab.iloc[:, 0]
                    variance = default_rates.var()
                    
                    interactions_summary[f"{var1}_x_{var2}"] = {
                        'type': 'categorical_x_categorical',
                        'variance_default_rate': round(variance, 2),
                        'n_combinations': len(crosstab)
                    }
                
                elif self.data[var1].dtype != 'object' and self.data[var2].dtype != 'object':
                    # Deux variables numériques
                    correlation = self.data[var1].corr(self.data[var2])
                    interactions_summary[f"{var1}_x_{var2}"] = {
                        'type': 'numerical_x_numerical',
                        'correlation': round(correlation, 3)
                    }
        
        self.report['advanced_analysis']['variable_interactions'] = interactions_summary
        
        print("   Principales interactions détectées:")
        for interaction, stats in list(interactions_summary.items())[:5]:
            if stats['type'] == 'categorical_x_categorical':
                print(f"   • {interaction}: Variance des taux = {stats['variance_default_rate']}")
            else:
                print(f"   • {interaction}: Corrélation = {stats['correlation']}")
    
    def _missing_patterns_analysis(self):
        """Analyse des patterns de données manquantes"""
        print("\n🕳️ Patterns des données manquantes")
        
        # Calculer les données manquantes par ligne
        missing_per_row = self.data.isnull().sum(axis=1)
        missing_per_col = self.data.isnull().sum()
        
        patterns_summary = {
            'rows_with_missing': int((missing_per_row > 0).sum()),
            'rows_with_missing_pct': round((missing_per_row > 0).mean() * 100, 2),
            'max_missing_per_row': int(missing_per_row.max()),
            'avg_missing_per_row': round(missing_per_row.mean(), 2),
            'cols_with_missing': int((missing_per_col > 0).sum()),
            'total_missing_values': int(self.data.isnull().sum().sum())
        }
        
        self.report['advanced_analysis']['missing_patterns'] = patterns_summary
        
        print(f"   • Lignes avec valeurs manquantes: {patterns_summary['rows_with_missing']} ({patterns_summary['rows_with_missing_pct']}%)")
        print(f"   • Colonnes avec valeurs manquantes: {patterns_summary['cols_with_missing']}")
        print(f"   • Total valeurs manquantes: {patterns_summary['total_missing_values']}")
        
        # Si il y a des données manquantes, créer une visualisation
        if patterns_summary['total_missing_values'] > 0:
            plt.figure(figsize=(12, 6))
            
            # Heatmap des données manquantes
            missing_matrix = self.data.isnull()
            if missing_matrix.any().any():
                import seaborn as sns
                sns.heatmap(missing_matrix, cbar=True, yticklabels=False, cmap='viridis')
                plt.title('PATTERN DES DONNÉES MANQUANTES', fontweight='bold')
                plt.xlabel('Variables')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(f"{self.output_dir}/patterns_donnees_manquantes.png", dpi=300, bbox_inches='tight')
                plt.close()
    
    def _stability_analysis(self):
        """Analyse de stabilité des variables (Population Stability Index)"""
        print("\n📈 Analyse de stabilité des variables")
        
        # Pour cette démonstration, on va simuler une analyse de stabilité
        # En production, on comparerait différentes périodes temporelles
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        stability_summary = {}
        
        for col in numeric_cols:
            # Diviser les données en deux parties (simulation de périodes différentes)
            split_point = len(self.data) // 2
            period1 = self.data[col].iloc[:split_point]
            period2 = self.data[col].iloc[split_point:]
            
            # Calculer des bins et des fréquences
            bins = np.linspace(self.data[col].min(), self.data[col].max(), 11)
            
            hist1, _ = np.histogram(period1.dropna(), bins=bins)
            hist2, _ = np.histogram(period2.dropna(), bins=bins)
            
            # Éviter la division par zéro
            hist1_pct = hist1 / max(hist1.sum(), 1)
            hist2_pct = hist2 / max(hist2.sum(), 1)
            
            # Calculer un PSI simplifié
            psi = 0
            for i in range(len(hist1_pct)):
                if hist1_pct[i] > 0 and hist2_pct[i] > 0:
                    psi += (hist2_pct[i] - hist1_pct[i]) * np.log(hist2_pct[i] / hist1_pct[i])
            
            stability_summary[col] = {
                'psi': round(psi, 4),
                'stability': 'Stable' if abs(psi) < 0.1 else 'Modérément instable' if abs(psi) < 0.25 else 'Instable'
            }
            
            print(f"   • {col.upper()}: PSI = {stability_summary[col]['psi']:.4f} ({stability_summary[col]['stability']})")
        
        self.report['advanced_analysis']['stability_analysis'] = stability_summary
    
    def generate_eda_report(self):
        """Génération du rapport EDA complet"""
        print("-" * 40)
        
        # Rapport texte détaillé
        report_path = f"{self.output_dir}/rapport_eda_complet.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RAPPORT D'ANALYSE EXPLORATOIRE DES DONNÉES (EDA)\n")
            f.write("SYSTÈME DE CRÉDIT SCORING\n")
            f.write("=" * 80 + "\n")
            f.write(f"Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Nombre total de clients : {len(self.data)}\n")
            f.write(f"Nombre de variables : {len(self.data.columns)}\n\n")
            
            # Résumé exécutif
            f.write("📋 RÉSUMÉ EXÉCUTIF\n")
            f.write("-" * 40 + "\n")
            target_dist = self.data['cible'].value_counts()
            f.write(f"• Distribution de la cible : {dict(target_dist)}\n")
            f.write(f"• Pourcentage de bons payeurs : {(target_dist.iloc[0]/len(self.data)*100):.1f}%\n")
            f.write(f"• Variables numériques : {len(self.data.select_dtypes(include=[np.number]).columns)}\n")
            f.write(f"• Variables catégorielles : {len(self.data.select_dtypes(include=['object']).columns)}\n\n")
            
            # Détails par section
            for section, content in self.report.items():
                if section == 'advanced_analysis':
                    f.write("🔬 ANALYSES AVANCÉES\n")
                    f.write("-" * 40 + "\n")
                    
                    # Outliers détaillés
                    if 'outliers_analysis' in content:
                        f.write("\n🔍 ANALYSE DES OUTLIERS :\n")
                        for var, stats in content['outliers_analysis'].items():
                            f.write(f"• {var.upper()}:\n")
                            f.write(f"  - IQR: {stats['iqr_outliers']} outliers ({stats['iqr_percentage']}%)\n")
                            f.write(f"  - Z-score: {stats['zscore_outliers']} outliers ({stats['zscore_percentage']}%)\n")
                            f.write(f"  - Percentiles: {stats['percentile_outliers']} outliers ({stats['percentile_percentage']}%)\n")
                    
                    # Clustering
                    if 'clustering_analysis' in content:
                        f.write("\n🎯 CLUSTERING DES CLIENTS :\n")
                        for cluster, stats in content['clustering_analysis'].items():
                            f.write(f"• {cluster}: {stats['size']} clients ({stats['percentage']}%)\n")
                            f.write(f"  - Taux de défaut: {stats['default_rate']}%\n")
                    
                    # Segmentation par risque
                    if 'risk_segmentation' in content:
                        f.write("\n📊 SEGMENTATION PAR RISQUE :\n")
                        for decile, stats in content['risk_segmentation'].items():
                            f.write(f"• {decile}: {stats['default_rate']}% défaut, {stats['avg_amount']}€ moyen, {stats['avg_duration']} mois\n")
                    
                    # Information mutuelle
                    if 'mutual_information' in content:
                        f.write("\n🧠 INFORMATION MUTUELLE (Top 10) :\n")
                        for i, var_info in enumerate(content['mutual_information'][:10]):
                            f.write(f"{i+1}. {var_info['Variable']}: {var_info['Mutual_Information']:.4f}\n")
                    
                    # Stabilité
                    if 'stability_analysis' in content:
                        f.write("\n📈 STABILITÉ DES VARIABLES :\n")
                        for var, stats in content['stability_analysis'].items():
                            f.write(f"• {var.upper()}: PSI = {stats['psi']} ({stats['stability']})\n")
                    
                    # Données manquantes
                    if 'missing_patterns' in content:
                        f.write("\n🕳️ DONNÉES MANQUANTES :\n")
                        patterns = content['missing_patterns']
                        f.write(f"• Lignes avec valeurs manquantes: {patterns['rows_with_missing']} ({patterns['rows_with_missing_pct']}%)\n")
                        f.write(f"• Colonnes avec valeurs manquantes: {patterns['cols_with_missing']}\n")
                        f.write(f"• Total valeurs manquantes: {patterns['total_missing_values']}\n")
                    
                    f.write("\n")
                else:
                    f.write(f"📊 {section.upper()}\n")
                    f.write("-" * 40 + "\n")
                    
                    if 'interpretations' in content:
                        f.write("INTERPRÉTATIONS :\n")
                        for key, interpretation in content['interpretations'].items():
                            f.write(f"• {key}: {interpretation}\n")
                    
                    f.write("\n")
            
            # Recommandations finales
            f.write("🎯 RECOMMANDATIONS POUR LA MODÉLISATION\n")
            f.write("-" * 40 + "\n")
            recommendations = self._generate_recommendations()
            for rec in recommendations:
                f.write(f"• {rec}\n")
        
        # Sauvegarde du rapport Python (pour usage ultérieur)
        import json
        with open(f"{self.output_dir}/rapport_eda_data.json", 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Rapport EDA sauvegardé :")
        print(f"   📄 Rapport texte : {report_path}")
        print(f"   📊 Graphiques : {self.output_dir}/*.png")
        print(f"   💾 Données : {self.output_dir}/rapport_eda_data.json")
    
    # === MÉTHODES D'INTERPRÉTATION AUTOMATIQUE ===
    
    def _interpret_numeric_distribution(self, col_name: str, series: pd.Series) -> str:
        """Interprétation automatique d'une distribution numérique"""
        mean_val = series.mean()
        median_val = series.median()
        std_val = series.std()
        
        if col_name == 'age':
            if mean_val < 30:
                return f"Population jeune (moyenne {mean_val:.0f} ans)"
            elif mean_val > 50:
                return f"Population âgée (moyenne {mean_val:.0f} ans)"
            else:
                return f"Population d'âge moyen (moyenne {mean_val:.0f} ans)"
        
        elif col_name == 'montant':
            if mean_val < 2000:
                return f"Petits montants de crédit (moyenne {mean_val:.0f}€)"
            elif mean_val > 5000:
                return f"Gros montants de crédit (moyenne {mean_val:.0f}€)"
            else:
                return f"Montants de crédit moyens (moyenne {mean_val:.0f}€)"
        
        elif col_name == 'duree':
            if mean_val < 12:
                return f"Crédits à court terme (moyenne {mean_val:.0f} mois)"
            elif mean_val > 24:
                return f"Crédits à long terme (moyenne {mean_val:.0f} mois)"
            else:
                return f"Crédits à moyen terme (moyenne {mean_val:.0f} mois)"
        
        else:
            return f"Moyenne: {mean_val:.2f}, Médiane: {median_val:.2f}, Écart-type: {std_val:.2f}"
    
    def _interpret_categorical_distribution(self, col_name: str, value_counts: pd.Series) -> str:
        """Interprétation automatique d'une distribution catégorielle"""
        most_frequent = value_counts.index[0]
        most_frequent_pct = (value_counts.iloc[0] / value_counts.sum()) * 100
        
        return f"Modalité dominante: '{most_frequent}' ({most_frequent_pct:.1f}%)"
    
    def _interpret_target_distribution(self, target_dist: pd.Series, target_pct: pd.Series) -> str:
        """Interprétation de la distribution de la variable cible"""
        categories = target_dist.index.tolist()
        
        if len(categories) == 2:
            good_pct = target_pct.iloc[0]
            if good_pct > 70:
                return f"Dataset déséquilibré : {good_pct:.1f}% de bons payeurs (risque de sur-apprentissage)"
            elif good_pct < 30:
                return f"Dataset déséquilibré : seulement {good_pct:.1f}% de bons payeurs"
            else:
                return f"Dataset équilibré : {good_pct:.1f}% de bons payeurs"
        
        return "Distribution de la variable cible analysée"
    
    def _interpret_numeric_vs_target(self, col_name: str, stats_by_target: pd.DataFrame) -> str:
        """Interprétation relation variable numérique vs cible"""
        means = stats_by_target['mean']
        diff_pct = abs((means.iloc[0] - means.iloc[1]) / means.mean()) * 100
        
        if diff_pct > 20:
            return f"Forte différence entre groupes ({diff_pct:.0f}% d'écart) - Variable discriminante"
        elif diff_pct > 10:
            return f"Différence modérée entre groupes ({diff_pct:.0f}% d'écart)"
        else:
            return f"Faible différence entre groupes ({diff_pct:.0f}% d'écart)"
    
    def _interpret_categorical_vs_target(self, col_name: str, crosstab: pd.DataFrame) -> str:
        """Interprétation relation variable catégorielle vs cible"""
        max_diff = crosstab.max(axis=1) - crosstab.min(axis=1)
        avg_diff = max_diff.mean()
        
        if avg_diff > 30:
            return f"Forte association avec la cible (écart moyen {avg_diff:.0f}%)"
        elif avg_diff > 15:
            return f"Association modérée avec la cible (écart moyen {avg_diff:.0f}%)"
        else:
            return f"Faible association avec la cible (écart moyen {avg_diff:.0f}%)"
    
    def _generate_recommendations(self) -> List[str]:
        """Génération de recommandations pour la modélisation"""
        recommendations = []
        
        # Analyse de la cible
        if 'target_analysis' in self.report:
            target_dist = self.report['target_analysis']['percentages']
            values = list(target_dist.values())
            if max(values) > 70:
                recommendations.append("Considérer des techniques de rééquilibrage (SMOTE, under-sampling)")
        
        # Analyse des corrélations
        if 'correlation' in self.report and self.report['correlation']['high_correlations']:
            recommendations.append("Attention aux variables fortement corrélées - risque de multicolinéarité")
        
        # Variables significatives
        if 'statistical_tests' in self.report:
            significant_vars = []
            for test_type in ['chi2_tests', 'ttest_results']:
                if test_type in self.report['statistical_tests']:
                    for var, result in self.report['statistical_tests'][test_type].items():
                        if result.get('significant', False):
                            significant_vars.append(var)
            
            if significant_vars:
                recommendations.append(f"Variables les plus discriminantes : {', '.join(significant_vars)}")
        
        # Recommandations générales
        recommendations.append("Effectuer un feature engineering sur les variables significatives")
        recommendations.append("Tester plusieurs algorithmes : Régression Logistique, Random Forest, XGBoost")
        recommendations.append("Utiliser une validation croisée stratifiée")
        
        return recommendations 