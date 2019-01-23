# Cloud SQL using Terraform

See the Cloud SQL documentation for details: https://cloud.google.com/sql

## Setting Up!

1. Create a bootstrap project (tf-bootstrap).
2. Enable the Cloud SQL Admin API.
3. Create a GCS bucket to hold the Terraform state (tf-bootstrap)
4. Create a service account and grant it the following roles:-
    * Cloud SQL Admin 
    * Storage Object Admin role.
5. Download the service account credentials to your machine.
6. Install Terraform (https://www.terraform.io/intro/getting-started/install.html) on your machine.
7. You are now ready to use Terraform on GCP!

## Running the Code

1. Go to the folder containing the code.
2. Set the proper values for all variables in the terraform.tfvars file.
3. Run 'terraform init' - This initializes a working directory containing Terraform config files.
    * Make sure to run 'gcloud init' before running 'terraform init'.
    * If terraform is unable to find default credentials, run 'gcloud auth application-default login' before 'terraform init'.
4. (Optional) Run 'terraform plan' - This displays a execution plan.
    * Can use the '-out' flag to store the plan in a file. 
5. Run 'terraform apply' - Applies the changes required to reach the desired state of the configuration.
6. Once completed, use the GCP console to check the creation of a Cloud SQL Master Instance.
7. Click on the instance and then click on Databases to check the creation of the database in the instance.
8. Run 'terraform destroy' - This command destroys the terraform-managed infrastucture.

## Using a Module

1. The code for using a module to run the code is shown below.
2. Assign values to required variables in the module declaration similar to assigning values in the "terraform.tfvars" file.

```
module "cloud_sql"{
    source = "./cloudsql"
    name = "example-mysqlmodule"
    credentials = "..."
    project = "..."
    region = "..."
    name = "..."
    database_version = "..."
    tier = "..."
    db_name = "..."
}
```

## Resources Created
1. google_sql_database_instance.master: The master database instance.
2. google_sql_database.default: The default database created.


## Inputs

Name | Description | Type | Default
---------|------------|:-------:|:-------:
credentials | The credentials file for the service account. | string | ""
project | The project in which the resource belongs, if not set the default provider project is used. | string | ""
region | Region for Cloud SQL instance. | string | us-central1
name | Name for the database instance. Must be unique and cannot be reused for up to one week. | string  | -
database_version | The version of of the database. For example, `MYSQL_5_6` or `POSTGRES_9_6`. | string | `MYSQL_5_6`
master_instance_name | The name of the master instance in the replication setup. | string | ""
tier | The machine tier (First Generation) or type (Second Generation). See this page for supported tiers and pricing: https://cloud.google.com/sql/pricing | string | `db-f1-micro`
db_name | Name of the database to create. | string | `default`
db_charset | The charset for the database. For MySQL see https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html. For Postgres see https://www.postgresql.org/docs/9.6/multibyte.html. | string | ""
db_collation | The collation for the default database. For MySQL see https://dev.mysql.com/doc/refman/5.7/en/charset-charsets.html. For Postgres see https://www.postgresql.org/docs/9.6/collation.html. | string | ""
activation_policy | This specifies when the instance should be active. Can be either `ALWAYS`, `NEVER` or `ON_DEMAND`. | string | `ALWAYS`
disk_autoresize | Second Generation only. Configuration to increase storage size automatically. | string | `true`
disl_size_gb | Second generation only. The size of data disk, in GB. Size of a running instance cannot be reduced but can be increased. | string | `10`
disk_type | Second generation only. The type of data disk: `PD_SSD` or `PD_HDD`. | string | `PD_SSD`
pricing_plan | First generation only. Pricing plan for this instance, can be one of `PER_USE` or `PACKAGE`. | string | `PER_USE`
replcation_type | Replication type for this instance, can be one of `ASYNCHRONOUS` or `SYNCHRONOUS`. | string | `SYNCHRONOUS`
database_flags | List of Cloud SQL flags that are applied to the database server | list | []