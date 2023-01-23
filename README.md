
# feur.

`feur.` est une application Flask permettant de créer des questionnaires, nottament des QCM.
Elle dispose d'un système de tags permettant d'organiser au mieux ses questions rédigées en markdown.
## Requirements

Pour déployer l'application :
+ git
+ python 3.10
+ pip

Pour faire fonctionner l'application :
+ Flask 2.2.2
+ flask_bcrypt 1.0.1
+ flask_login 0.6.2
+ flask_sqlalchemy 3.0.2
+ flask_wtf 1.1.1
+ mistune 2.0.4
+ Pygments 2.14.0
+ WTForms 3.0.1
## Deployment

Pour déployer le projet :

```bash
  git clone https://github.com/ArnaudPeler/Projet-Programation-L2-Groupe-31.git
  cd Projet-Programation-L2-Groupe-31
  pip install -r requirements.txt
```

Pour lancer l'application :
```bash
python3 app.py
```
## FAQ

#### Comment sont gérées les questions ?

Chaque question existe dans un fichier markdown `.md` sur le serveur.
Chaque note n'appartient qu'à un utilisateur et seul lui peut la modifier ou la supprimer.
L'application permet aussi de créer des notes et de les éditer directement sur le serveur grâce à un éditeur markdown sommaire.


#### Quelles fonctionnalités markdown sont disponibles ?

+ [Toutes les fonctionnalités de base de markdown](https://www.markdownguide.org/basic-syntax/)
+ [Syntax Highlighting pour le code](https://www.markdownguide.org/extended-syntax/#syntax-highlighting)
+ [MathJax pour les formules mathématiques (LaTeX)](https://www.mathjax.org/)
+ [Mermaid pour les graph](https://mermaid.js.org/)

#### Comment sont gérés les tags/étiquette ?
Les tags se définissent dans la première ligne du markdown de la question avec le caractère `@`

Exemple, un fichier commençant par
```markdown
@C++ @Systèmes
```
possède les tags `C++` et `Systèmes`

##### Comment indiquer les réponses à la question
Dans le markdown de la question, vous pouvez délimiter un "bloc réponses" avec :
````markdown
``` reponses
+ Bonne réponse
Mauvaise réponse
+ Une autre réponse
``` 
````
Et correspondra en html à :
```html
<form>
    <input type="checkbox" name="trueAnswer_0" id="0">
    <label for="0">Bonne réponse</label><br>
    <input type="checkbox" id="1">
    <label for="1">Mauvaise réponse</label><br>
    <input type="checkbox" name="trueAnswer_2" id="2">
    <label for="2">Une autre réponse</label><br>
</form>
```
et sera représenté par des cases à cocher dans la version imprimable

#### Comment assembler les questions dans un questionnaire ?
Sélectionnez toutes les questions que vous voulez assembler et appuyez sur le bouton `Aggregate`, vous pouvez ensuite nommer le questionnaire et l'imprimer.
## Authors

- [@ArnaudPeler](https://github.com/ArnaudPeler)
- [@alderaan11](https://github.com/alderaan11)
- [@Mxckx9772](https://github.com/Mxckx9772)
- [@pchtpcht](https://github.com/pchtpcht)

## License

[MIT](https://choosealicense.com/licenses/mit/)

