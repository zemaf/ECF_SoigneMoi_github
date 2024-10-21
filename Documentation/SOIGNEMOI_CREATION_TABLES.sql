------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------



------------------------------------------------------------
-- Table: administrateur
------------------------------------------------------------
CREATE TABLE public.administrateur(
	admin_id   SERIAL NOT NULL ,
	nom        VARCHAR (50) NOT NULL ,
	prenom     VARCHAR (50) NOT NULL ,
	email      VARCHAR (100) NOT NULL  ,
	CONSTRAINT administrateur_PK PRIMARY KEY (admin_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: medicament
------------------------------------------------------------
CREATE TABLE public.medicament(
	medicament_id   SERIAL NOT NULL ,
	nom             VARCHAR (100) NOT NULL ,
	psologie        VARCHAR (255) NOT NULL  ,
	CONSTRAINT medicament_PK PRIMARY KEY (medicament_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: utilisateur
------------------------------------------------------------
CREATE TABLE public.utilisateur(
	user_id        SERIAL NOT NULL ,
	nom            VARCHAR (50) NOT NULL ,
	prenom         VARCHAR (50) NOT NULL ,
	adresse        VARCHAR (100) NOT NULL ,
	email          VARCHAR (50) NOT NULL ,
	mot_de_passe   VARCHAR (255) NOT NULL  ,
	CONSTRAINT utilisateur_PK PRIMARY KEY (user_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: specialite
------------------------------------------------------------
CREATE TABLE public.specialite(
	specialite_id   SERIAL NOT NULL ,
	nom             VARCHAR (50) NOT NULL  ,
	CONSTRAINT specialite_PK PRIMARY KEY (specialite_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: medecin
------------------------------------------------------------
CREATE TABLE public.medecin(
	medecin_id      SERIAL NOT NULL ,
	matricule       VARCHAR (50) NOT NULL ,
	nom             VARCHAR (50) NOT NULL ,
	prenom          VARCHAR (50) NOT NULL ,
	specialite_id   INT  NOT NULL ,
	admin_id        INT  NOT NULL  ,
	CONSTRAINT medecin_PK PRIMARY KEY (medecin_id)

	,CONSTRAINT medecin_specialite_FK FOREIGN KEY (specialite_id) REFERENCES public.specialite(specialite_id)
	,CONSTRAINT medecin_administrateur0_FK FOREIGN KEY (admin_id) REFERENCES public.administrateur(admin_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: avis
------------------------------------------------------------
CREATE TABLE public.avis(
	avis_id       SERIAL NOT NULL ,
	libelle       VARCHAR (255) NOT NULL ,
	date          DATE  NOT NULL ,
	description   VARCHAR (2000)  NOT NULL ,
	medecin_id    INT  NOT NULL ,
	user_id       INT  NOT NULL  ,
	CONSTRAINT avis_PK PRIMARY KEY (avis_id)

	,CONSTRAINT avis_medecin_FK FOREIGN KEY (medecin_id) REFERENCES public.medecin(medecin_id)
	,CONSTRAINT avis_utilisateur0_FK FOREIGN KEY (user_id) REFERENCES public.utilisateur(user_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: prescription
------------------------------------------------------------
CREATE TABLE public.prescription(
	prescription_id         SERIAL NOT NULL ,
	date_debut_traitement   DATE  NOT NULL ,
	date_fin_traitement     DATE  NOT NULL ,
	medecin_id              INT  NOT NULL ,
	user_id                 INT  NOT NULL  ,
	CONSTRAINT prescription_PK PRIMARY KEY (prescription_id)

	,CONSTRAINT prescription_medecin_FK FOREIGN KEY (medecin_id) REFERENCES public.medecin(medecin_id)
	,CONSTRAINT prescription_utilisateur0_FK FOREIGN KEY (user_id) REFERENCES public.utilisateur(user_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: sejour
------------------------------------------------------------
CREATE TABLE public.sejour(
	sejour_id     SERIAL NOT NULL ,
	date_entree   DATE  NOT NULL ,
	date_sortie   DATE  NOT NULL ,
	motif         VARCHAR (2000)  NOT NULL ,
	user_id       INT  NOT NULL ,
	medecin_id    INT  NOT NULL  ,
	CONSTRAINT sejour_PK PRIMARY KEY (sejour_id)

	,CONSTRAINT sejour_utilisateur_FK FOREIGN KEY (user_id) REFERENCES public.utilisateur(user_id)
	,CONSTRAINT sejour_medecin0_FK FOREIGN KEY (medecin_id) REFERENCES public.medecin(medecin_id)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: contient
------------------------------------------------------------
CREATE TABLE public.contient(
	medicament_id     INT  NOT NULL ,
	prescription_id   INT  NOT NULL  ,
	CONSTRAINT contient_PK PRIMARY KEY (medicament_id,prescription_id)

	,CONSTRAINT contient_medicament_FK FOREIGN KEY (medicament_id) REFERENCES public.medicament(medicament_id)
	,CONSTRAINT contient_prescription0_FK FOREIGN KEY (prescription_id) REFERENCES public.prescription(prescription_id)
)WITHOUT OIDS;



