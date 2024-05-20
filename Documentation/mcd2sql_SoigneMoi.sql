------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------



------------------------------------------------------------
-- Table: administrateur
------------------------------------------------------------
CREATE TABLE public.administrateur(
	matricule   VARCHAR (255) NOT NULL ,
	nom         VARCHAR (50) NOT NULL ,
	prenom      VARCHAR (50) NOT NULL ,
	email       VARCHAR (100) NOT NULL  ,
	CONSTRAINT administrateur_PK PRIMARY KEY (matricule)
);


------------------------------------------------------------
-- Table: medicament
------------------------------------------------------------
CREATE TABLE public.medicament(
	medicament_id   SERIAL NOT NULL ,
	nom             VARCHAR (100) NOT NULL ,
	psologie        VARCHAR (255) NOT NULL  ,
	CONSTRAINT medicament_PK PRIMARY KEY (medicament_id)
);


------------------------------------------------------------
-- Table: utilisateur
------------------------------------------------------------
CREATE TABLE public.utilisateur(
	user_id        SERIAL NOT NULL ,
	nom            VARCHAR (100) NOT NULL ,
	prenom         VARCHAR (100) NOT NULL ,
	adresse        VARCHAR (100) NOT NULL ,
	email          VARCHAR (100) NOT NULL ,
	mot_de_passe   VARCHAR (255) NOT NULL  ,
	CONSTRAINT utilisateur_PK PRIMARY KEY (user_id)
);

------------------------------------------------------------
-- Table: specialite
------------------------------------------------------------
CREATE TABLE public.specialite(
	specialite_id   SERIAL NOT NULL ,
	nom             VARCHAR (50) NOT NULL  ,
	CONSTRAINT specialite_PK PRIMARY KEY (specialite_id)
);


------------------------------------------------------------
-- Table: medecin
------------------------------------------------------------
CREATE TABLE public.medecin(
	matricule                  SERIAL NOT NULL ,
	nom                        VARCHAR (100) NOT NULL ,
	prenom                     VARCHAR (100) NOT NULL ,
	specialite                 VARCHAR (100) NOT NULL ,
	specialite_id              INT  NOT NULL ,
	matricule_administrateur   VARCHAR (255) NOT NULL  ,
	CONSTRAINT medecin_PK PRIMARY KEY (matricule)

	,CONSTRAINT medecin_specialite_FK FOREIGN KEY (specialite_id) REFERENCES public.specialite(specialite_id)
	,CONSTRAINT medecin_administrateur0_FK FOREIGN KEY (matricule_administrateur) REFERENCES public.administrateur(matricule)
);


------------------------------------------------------------
-- Table: avis
------------------------------------------------------------
CREATE TABLE public.avis(
	avis_id       INT  NOT NULL ,
	user_id       INT  NOT NULL ,
	user          VARCHAR (100) NOT NULL ,
	libelle       VARCHAR (255) NOT NULL ,
	date          DATE  NOT NULL ,
	description   VARCHAR (2000)  NOT NULL ,
	matricule     INT  NOT NULL  ,
	CONSTRAINT avis_PK PRIMARY KEY (avis_id,user_id)

	,CONSTRAINT avis_medecin_FK FOREIGN KEY (matricule) REFERENCES public.medecin(matricule)
);


------------------------------------------------------------
-- Table: prescription
------------------------------------------------------------
CREATE TABLE public.prescription(
	prescription_id         INT  NOT NULL ,
	user_id                 INT  NOT NULL ,
	date_debut_traitement   DATE  NOT NULL ,
	date_fin_traitement     DATE  NOT NULL ,
	matricule               INT  NOT NULL  ,
	CONSTRAINT prescription_PK PRIMARY KEY (prescription_id,user_id)

	,CONSTRAINT prescription_medecin_FK FOREIGN KEY (matricule) REFERENCES public.medecin(matricule)
);


------------------------------------------------------------
-- Table: sejour
------------------------------------------------------------
CREATE TABLE public.sejour(
	sejour_id       SERIAL NOT NULL ,
	date_entree     DATE  NOT NULL ,
	date_sortie     DATE  NOT NULL ,
	motif           VARCHAR (2000)  NOT NULL ,
	medecin         VARCHAR (100) NOT NULL ,
	user_id         INT  NOT NULL ,
	specialite_id   INT  NOT NULL  ,
	CONSTRAINT sejour_PK PRIMARY KEY (sejour_id)

	,CONSTRAINT sejour_utilisateur_FK FOREIGN KEY (user_id) REFERENCES public.utilisateur(user_id)
	,CONSTRAINT sejour_specialite0_FK FOREIGN KEY (specialite_id) REFERENCES public.specialite(specialite_id)
);


------------------------------------------------------------
-- Table: emploi_du_temps
------------------------------------------------------------
CREATE TABLE public.emploi_du_temps(
	edt_id                 SERIAL NOT NULL ,
	libelle_intervention   VARCHAR (255) NOT NULL ,
	date                   DATE  NOT NULL ,
	matricule              INT  NOT NULL  ,
	CONSTRAINT emploi_du_temps_PK PRIMARY KEY (edt_id)

	,CONSTRAINT emploi_du_temps_medecin_FK FOREIGN KEY (matricule) REFERENCES public.medecin(matricule)
);


------------------------------------------------------------
-- Table: contient
------------------------------------------------------------
CREATE TABLE public.contient(
	medicament_id     INT  NOT NULL ,
	prescription_id   INT  NOT NULL ,
	user_id           INT  NOT NULL  ,
	CONSTRAINT contient_PK PRIMARY KEY (medicament_id,prescription_id,user_id)

	,CONSTRAINT contient_medicament_FK FOREIGN KEY (medicament_id) REFERENCES public.medicament(medicament_id)
	,CONSTRAINT contient_prescription0_FK FOREIGN KEY (prescription_id,user_id) REFERENCES public.prescription(prescription_id,user_id)
);



