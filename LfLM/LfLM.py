from io import StringIO

import vertexai
import vertexai.preview.generative_models as generative_models
from google.cloud import bigquery
from vertexai.generative_models import GenerativeModel

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# text1 = """write an SQL query for the GCP bigquery billing export to answer the following question:
# how much did I spend on N1 cpus  last month?"""

text1 = """write an SQL query for the GCP bigquery billing export to answer the following question:
how much did the spend on N1 cpus change for the last 10 days?"""

text2 = "Explain the following bigquery billing query result, the original question was {}. The query result is:".format(
    text1)


def run_bigquery_query(sql, project_id):
    # Build the BigQuery client object
    client = bigquery.Client(project=project_id)

    # Set the dataset where the tables are located

    # Define the query job
    query_job = client.query(sql)

    # Run the query and get results
    try:
        query_results = query_job.result()  # Waits for job to complete
        field_names = [field.name for field in query_results.schema]
        rows = [dict(row) for row in query_results]  # Convert row results to dictionaries

        # Create a StringIO object to capture output
        output = StringIO()
        output.write(','.join(field_names) + '\n')  # Write column headers to the output

        for row in rows:
            # Join column values with a comma (",") and add a newline character ("\n") at the end
            output.write(','.join(str(v) for v in row.values()) + '\n')

        # Return the content of the StringIO object as a string
        return output.getvalue()


    except Exception as e:
        print(f"Error running BigQuery query: {e}")
        return None


def generate(txt):
    vertexai.init(project="", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-pro-preview-0514",
        system_instruction=["""generate only valid sql and no markdown. The table is <>


    stracture of the table:
    Field	Type	Description
billing_account_id	String
The Cloud Billing account ID that the usage is associated with.

For resellers: For usage costs generated by a Cloud Billing subaccount, this is the ID of the subaccount, not the ID of the parent reseller Cloud Billing account.

invoice.month	String
The year and month (YYYYMM) of the invoice that includes the cost line items. For example: "201901" is equivalent to January, 2019.

You can use this field to get the total charges on the invoice. See Cloud Billing Export to BigQuery Query Examples.

Note: The first full month of data with this field is June 2018.
Be aware: The invoice month may differ from the usage month. For example, some product usage at the very end of a month may be charged to the next month's invoice. Also, the invoice month for Cloud Billing adjustments and associated taxes reflects the month the adjustment was issued; the adjustment could be applied to a different month than the issue month. Refer to errors and adjustments for more information.
cost_type	String
The type of cost this line item represents: regular, tax, adjustment, or rounding error.

Notes:
The first full month of data with this field is January 2019.
Starting on September 1, 2020, you see a separate line item for taxes, for each of your projects.
service.id	String	The ID of the service that the usage is associated with.
service.description	String	The Google Cloud service that reported the Cloud Billing data.
sku.id	String	The ID of the resource used by the service. For the full list of SKUs, see Google Cloud SKUs.
Note: You can use the sku.id column to map each of your line items to the list prices published on the Google Cloud pricing pages, in the Pricing Table report, and through the Cloud Billing Catalog API.
sku.description	String	A description of the resource type used by the service. For example, a resource type for Cloud Storage is Standard Storage US.
usage_start_time	Timestamp	The start time of the hourly usage window within which the given cost was calculated. The usage/costs for all services is displayed with hourly granularity, which means long running service usage is spread across multiple hourly windows.
For more information, see the BigQuery documentation on timestamp data types. See also, Differences between exported data and invoices below.

usage_end_time	Timestamp	The end time of the hourly usage window within which the given cost was calculated. The usage/costs for all services is displayed with hourly granularity, which means long running service usage is spread across multiple hourly windows.
For more information, see the BigQuery documentation on timestamp data types. See also, Differences between exported data and invoices below.

project	Struct	project contains fields that describe the Cloud Billing project, such as ID, number, name, ancestry_numbers, and labels.
Be aware: For newly created projects, project information might not be present on usage that occurs within 24 hours of project creation.
project.id	String	The ID of the Google Cloud project that generated the Cloud Billing data.
project.number	String	An internally-generated, anonymized, unique identifier for the Google Cloud project that generated the Cloud Billing data. In your support cases and other customer communication, Google will refer to your projects by this project number.
Note: The first full day of data for this field is October 29, 2020.
For examples of how to manage your Cloud Billing data exports to BigQuery after the schema update, see Handling schema changes to BigQuery export data tables.

project.name	String	The name of the Google Cloud project that generated the Cloud Billing data.
project.ancestry_numbers	String	The ancestors in the resource hierarchy for the project identified by the specified project.id (for example, my-project-123).
For example: /ParentOrgNumber/ParentFolderNumber/. Learn more about the Resource Hierarchy.

Note: During Cloud Billing data export, project ancestry is recorded based on the time of usage. Organization and folder numbers are immutable, however, a project's ancestry is not. Over time, you might move projects and folders around in your resource hierarchy. The first full month of data with this field is January 2019.
project.ancestors	Struct
This field describes the structure and value of the resource hierarchy of a cost line item, including projects, folders, and organizations. Ancestors are ordered from node to root (project, folder, then organization).

Note: The first full month of data for this field is April 2022.
project.ancestors.resource_name	String	The relative resource name for each ancestor in the format 'resourceType/resourceNumber'. Using project.ancestors.resource_name will offer a more complete view of project.ancestry_numbers.
project.ancestors.display_name	String	The name that you have created for your resource in your console.
project.labels.key	String	If labels are present, the key portion of the key:value pair that comprises the label on the Google Cloud project where the usage occurred. For more information about using labels, see Using Labels.
project.labels.value	String	If labels are present, the value portion of the key:value pair that comprises the label on the Google Cloud project where the usage occurred. For more information about using labels, see Using Labels.
labels.key	String	If labels are present, the key portion of the key:value pair that comprises the label on the Google Cloud resource where the usage occurred. For more information about using labels, see Using Labels.
labels.value	String	If labels are present, the value portion of the key:value pair that comprises the label on the Google Cloud resource where the usage occurred. For more information about using labels, see Using Labels.
system_labels.key	String	If system labels are present, the key portion of the key:value pair that comprises the system-generated label on the resource where the usage occurred. See also, Available system labels.
Note: The first full day of data with this field is September 18, 2018.
system_labels.value	String	If system labels are present, the value portion of the key:value pair that comprises the system-generated label on the resource where the usage occurred. See also, Available system labels.
Note: The first full day of data with this field is September 18, 2018.
location.location	String	Location of usage at the level of a multi-region, country, region, or zone; or global for resources that have no specific location. For more information, see Geography and regions and Google Cloud locations.
Note: The first full day of data with this field is September 18, 2018.
location.country	String	When location.location is a country, region, or zone, this field is the country of usage, e.g. US. For more information, see Geography and regions and Google Cloud locations.
Note: The first full day of data with this field is September 18, 2018.
location.region	String	When location.location is a region or zone, this field is the region of usage, e.g. us-central1. For more information, see Geography and regions and Google Cloud locations.
Note: The first full day of data with this field is September 18, 2018.
location.zone	String	When location.location is a zone, this field is the zone of usage, e.g. us-central1-a. For more information, see Geography and regions and Google Cloud locations.
Note: The first full day of data with this field is September, 18 2018.
cost	Float	The cost of the usage before any credits, to a precision of up to six decimal places. To get the total cost including credits, any credits.amount should be added to cost. See this example query for more information.
currency	String	The currency that the cost is billed in. For more information, see Local Currency for Billing and Payments.
currency_conversion_rate	Float	The exchange rate from US dollars to the local currency. That is, cost ÷ currency_conversion_rate is the cost in US dollars.
Note: When Google charges in local currency, we convert prices into applicable local currency pursuant to the conversion rates published by leading financial institutions.
usage.amount	Float	The quantity of usage.unit used.
usage.unit	String	The base unit in which resource usage is measured. For example, the base unit for standard storage is byte-seconds.
usage.amount_in_pricing_units	Float	The quantity of usage.pricing_unit used.
Note: The first full day of data with this field is January 22, 2018.
usage.pricing_unit	String	The unit in which resource usage is measured, according to the Cloud Billing Catalog API.
Note: The first full day of data with this field is January 22, 2018.
credits	Struct	credits contains fields that describe the structure and value of the credits associated with Google Cloud and Google Maps Platform SKUs.
credits.id	String	If present, indicates that a credit is associated with the product SKU. credits.id values are either an alphanumeric unique identifier (for example, 12-b34-c56-d78), or a description of the credit type (such as Committed Usage Discount: CPU).
If the credits.id field is empty, then the product SKU is not associated with a credit.

Note: The first full day of data with this field is September 10, 2020.
credits.full_name	String	The name of the credit associated with the product SKU. This is a human-readable description of an alphanumeric credits.id. Examples include Free trial credit or Spend-based committed use discount.
credits.full_name values are only present for SKUs with an alphanumeric credits.id. If the value of the credits.id is a description of the credit type (such as Committed Usage Discount: CPU), then the credits.full_name field will be empty.

Note: The first full day of data with this field is September 10, 2020.
credits.type	String	This field describes the purpose or origin of the credits.id. Credit types include:
COMMITTED_USAGE_DISCOUNT: Resource-based committed use contracts purchased for Compute Engine in return for deeply discounted prices for VM usage.
COMMITTED_USAGE_DISCOUNT_DOLLAR_BASE: Spend-based committed use contracts purchased for services in exchange for your commitment to spend a minimum amount.
DISCOUNT: The discount credit type is used for credits earned after a contractual spending threshold is reached. Note that in the Cloud Billing reports available in the Google Cloud console, the discount credit type is listed as Spending based discounts (contractual).
FREE_TIER: Some services offer free resource usage up to specified limits. For these services, credits are applied to implement the free tier usage.
PROMOTION: The promotion credit type includes Google Cloud Free Trial and marketing campaign credits, or other grants to use Google Cloud. When available, promotional credits are considered a form of payment and are automatically applied to reduce your total bill.
RESELLER_MARGIN: If you are a reseller, the reseller margin credit type indicates the Reseller Program Discounts earned on every eligible line item.
SUBSCRIPTION_BENEFIT: Credits earned by purchasing long-term subscriptions to services in exchange for discounts.
SUSTAINED_USAGE_DISCOUNT: The sustained use discounts credit type is an automatic discount that you earn for running specific Compute Engine resources for a significant portion of the billing month.
Note: The first full day of data with this field is September 10, 2020.
credits.name	String	A description of the credit applied to the Cloud Billing account.
credits.amount	Float	The amount of the credit applied to the usage.
adjustment_info	Struct	adjustment_info contains fields that describe the structure and value of an adjustment to cost line items associated with a Cloud Billing account.
adjustment_info values are only present if the cost line item was generated for a Cloud Billing modification. A modification can happen for correction or non-correction reasons. The adjustment_info type contains details about the adjustment, whether it was issued for correcting an error or other reasons.

Note: The first full day of data for this field is October 29, 2020.
For examples of how to manage your Cloud Billing data exports to BigQuery after the schema update, see Handling schema changes to BigQuery export data tables.

adjustment_info.id	String	If present, indicates that an adjustment is associated with a cost line item. adjustment_info.id is the unique ID for all the adjustments associated caused by an issue.
adjustment_info.description	String	A description of the adjustment and its cause.
adjustment_info.type	String
The type of adjustment.

Types include:

USAGE_CORRECTION: A correction due to incorrect reported usage.
PRICE_CORRECTION: A correction due to incorrect pricing rules.
METADATA_CORRECTION: A correction to fix metadata without changing the cost.
GOODWILL: A credit issued to the customer for goodwill.
SALES_BASED_GOODWILL: A credit issued to the customer for goodwill, as part of a contract.
SLA_VIOLATION: A credit issued to the customer due to a service-level objective (SLO) violation.
BALANCE_TRANSFER: An adjustment to transfer funds from one payment account to another.
ACCOUNT_CLOSURE: An adjustment to bring a closed account to a zero balance.
GENERAL_ADJUSTMENT: A general billing account modification.
adjustment_info.mode	String
How the adjustment was issued.

Modes include:

PARTIAL_CORRECTION: The correction partially negates the original usage and cost.
COMPLETE_NEGATION_WITH_REMONETIZATION: The correction fully negates the original usage and cost, and issues corrected line item(s) with updated usage and cost.
COMPLETE_NEGATION: The correction fully negates the original usage and cost, and no further usage is remonetized.
MANUAL_ADJUSTMENT: The adjustment is allocated to cost and usage manually.
export_time	Timestamp	A processing time associated with an append of Cloud Billing data. This will always increase with each new export.
Note: Use the export_time column to understand when the exported billing data was last updated.
See also, Differences between exported data and invoices below.
tags	Struct
Fields that describe the tag, such as key, value, and namespace.

Note: The first full month of data with these tags is October 2022.
tags.key	String
The short name or display name of the key associated with this particular tag.

tags.value	String
The resources attached to a tags.key. At any given time, exactly one value can be attached to a resource for a given key.

tags.inherited	Boolean
Indicates whether a tag binding is inherited (Tags Inherited = True) or direct/non-inherited (Tags Inherited = False). You can create a tag binding to a parent resource in the resource hierarchy.

tags.namespace	String
Represents the resource hierarchy that define tag key and values. Namespace can be combined with tag key and tag value short names to create a globally unique, fully qualified name for the tag key or tag value.

cost_at_list	Float
The list prices associated with all line items charged to your Cloud Billing account.

Note: The first full day of data with this field is June 29, 2023.
transaction_type	String
The transaction type of the seller. The transaction type might be one of the following:

GOOGLE = 1: Services sold by Google Cloud.
THIRD_PARTY_RESELLER = 2: Third party services resold by Google Cloud.
THIRD_PARTY_AGENCY = 3: Third party services sold by a partner, with Google Cloud acting as the agent.
Note: The first full day of data with this field is August 22, 2023.
seller_name	String
The legal name of the seller.

Note: The first full day of data with this field is August 22, 2023."""]

    )
    responses = model.generate_content(
        [txt],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )

    return responses.text


query = generate(text1).replace('```sql', '').replace('```', '').replace('\\', '')
rows = run_bigquery_query(query, 'wideops-billing')

pass
if rows is not None:
    output = generate(text2 + '$' + str(rows)
                      )

    pass

    print(output)
else:
    print('Oops! Something went wrong. Please try again.')
